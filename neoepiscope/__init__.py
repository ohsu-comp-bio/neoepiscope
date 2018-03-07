#!/usr/bin/env python
"""
neoepiscope

Identifies neoepitopes from DNA-seq, VCF, GTF, and Bowtie index.
"""
from __future__ import print_function
import argparse
import bowtie_index
import sys
import string
import copy
import pickle
import copy
import os
import random
import re
import collections
import tempfile
import subprocess
import warnings
import exe_paths
from transcript import (Transcript, gtf_to_cds, cds_to_tree,
                        get_transcripts_from_tree, process_haplotypes,
                        get_peptides_from_transcripts)
from binding_scores import (gather_binding_scores, get_affinity_mhcflurry, 
                            get_affinity_netMHCpan, get_affinity_netMHCIIpan)
from file_processing import (adjust_tumor_column, combine_vcf, 
                                prep_hapcut_output, which, get_VAF_pos,
                                write_results)
from operator import itemgetter
from intervaltree import Interval, IntervalTree

_help_intro = '''neoepiscope searches for neoepitopes in seq data.'''

def help_formatter(prog):
    """ So formatter_class's max_help_position can be changed. """
    return argparse.HelpFormatter(prog, max_help_position=40)

def main():
    """ Entry point for neoepiscope software """
    parser = argparse.ArgumentParser(description=_help_intro, 
                                        formatter_class=help_formatter)
    subparsers = parser.add_subparsers(help=(
                                    'subcommands; add "-h" or "--help" '
                                    'after a subcommand for its parameters'
                                ), dest='subparser_name')
    index_parser = subparsers.add_parser('index',
                                        help=('produces pickled dictionaries '
                                        'linking transcripts to intervals and '
                                        ' CDS lines in a GTF'))
    swap_parser = subparsers.add_parser('swap',
                                        help=('swaps tumor and normal columns '
                                        'in a somatic vcf if necessary for '
                                        'proper HapCUT2 results'))
    merge_parser = subparsers.add_parser('merge',
                                         help=('merges germline and somatic '
                                               'VCFS for combined mutation '
                                               'phasing with HAPCUT2'))
    prep_parser = subparsers.add_parser('prep',
                                        help=('combines HAPCUT2 output with '
                                              'unphased variants for call '
                                              'mode'))
    call_parser = subparsers.add_parser('call', help='calls neoepitopes')
    # Index parser options (produces pickled dictionaries for transcript data)
    index_parser.add_argument('-g', '--gtf', type=str, required=True,
            help='input path to GTF file'
        )  
    index_parser.add_argument('-d', '--dicts', type=str, required=True,
            help='output path to pickled CDS dictionary directory'
        )
    # Swap parser options (swaps columns in somatic VCF)
    swap_parser.add_argument('-i', '--input', type=str, required=True,
            help='input path to somatic VCF'
        )
    swap_parser.add_argument('-o', '--output', type=str, required=False,
            help='output path to column-swapped VCF'
        )
    # Merger parser options (merges somatic and germline VCFs)
    merge_parser.add_argument('-g', '--germline', type=str, required=True,
            help='input path to germline VCF'
        )
    merge_parser.add_argument('-s', '--somatic', type=str, required=True,
            help='input path to somatic VCF'
        )
    merge_parser.add_argument('-o', '--output', type=str, required=False,
            help='output path to combined VCF'
        )
    # Prep parser options (adds unphased mutations as their own haplotype)
    prep_parser.add_argument('-v', '--vcf', type=str, required=True,
            help='input VCF'
        )
    prep_parser.add_argument('-c', '--hapcut2-output', type=str, required=True,
            help='path to output file of HAPCUT2 run on input VCF'
        )
    prep_parser.add_argument('-o', '--output', type=str, required=True,
            help='path to output file to be input to call mode'
        )
    # Call parser options (calls neoepitopes)
    call_parser.add_argument('-x', '--bowtie-index', type=str, required=True,
            help='path to Bowtie index basename'
        )
    call_parser.add_argument('-v', '--vcf', type=str, required=True,
            help='input path to VCF'
        )
    call_parser.add_argument('-d', '--dicts', type=str, required=True,
            help='input path to pickled CDS dictionary directory'
        )
    call_parser.add_argument('-c', '--merged-hapcut2-output', type=str,
            required=True,
            help='path to output of prep subcommand'
        )
    call_parser.add_argument('-k', '--kmer-size', type=str, required=False,
            default='8,11', help='kmer size for epitope calculation'
        )
    call_parser.add_argument('-p', '--affinity-predictor', type=str, 
            nargs=3, required=False, action='append', 
            default=[['mhcflurry', '1', 'affinity,rank']],
            help='binding affinity prediction software,'
                'associated version number, and scoring method(s) '
                '(e.g. -p netMHCpan 4 rank,affinity); '
                'for multiple softwares, repeat the argument;'
                'see documentation for details'
        )
    call_parser.add_argument('-a', '--alleles', type=str, required=True,
            help='comma separated list of alleles; '
                 'see documentation online for more information'
        )
    call_parser.add_argument('-o', '--output_file', type=str, required=True,
            help='path to output file'
        )
    call_parser.add_argument('-u', '--upstream_atgs', type=str, required=False,
            default='novel', help='how to handle upstream start codons, see '
            'documentation online for more information'
        )
    call_parser.add_argument('-g', '--germline', type=str, required=False,
            default='background', help='how to handle germline mutations in '
            'neoepitope enumeration; documentation online for more information'
        )
    call_parser.add_argument('-s', '--somatic', type=str, required=False,
            default='include', help='how to handle somatic mutations in '
            'neoepitope enumeration; documentation online for more information'
        )
    args = parser.parse_args()
    if args.subparser_name == 'index':
        cds_dict = gtf_to_cds(args.gtf, args.dicts)
        tree = cds_to_tree(cds_dict, args.dicts)
    elif args.subparser_name == 'swap':
        adjust_tumor_column(args.input, args.output)
    elif args.subparser_name == 'merge':
        combine_vcf(args.germline, args.somatic, outfile=args.output)
    elif args.subparser_name == 'prep':
        prep_hapcut_output(args.output, args.hapcut2_output, args.vcf)
    elif args.subparser_name == 'call':
        # Load pickled dictionaries
        with open(os.path.join(
                    args.dicts, 'intervals_to_transcript.pickle'
                ), 'rb') as interval_stream:
            interval_dict = pickle.load(interval_stream)
        with open(os.path.join(
                    args.dicts, 'transcript_to_CDS.pickle'
                ), 'rb') as cds_stream:
            cds_dict = pickle.load(cds_stream)
        # Check affinity predictor
        tool_dict = {}
        if args.affinity_predictor is not None:
            for tool in args.affinity_predictor:
                program = tool[0]
                version = tool[1]
                scoring = tool[2].split(',')
                if 'mhcflurry' in program:
                    if version == '1' and 'mhcflurry1' not in tool_dict:
                        program = 'mhcflurry-predict'
                        acceptable_scoring = ['rank', 'affinity', 
                                                            'high', 'low']
                        for method in scoring:
                            if method not in acceptable_scoring:
                                warnings.warn(' '.join([method, 
                                        'not compatible with mhcflurry']),
                                        Warning)
                                scoring.remove(method)
                        if len(scoring) > 0:
                            tool_dict['mhcflurry1'] = [program,
                                                            sorted(scoring)]
                    elif 'mhcflurry1' in tool_dict:
                        raise RuntimeError('Conflicting or repetitive installs'
                                            'of mhcflurry given')
                    else:
                        raise NotImplementedError(
                            ' '.join(['Neoepiscope does not support version', 
                                      version, 'of mhcflurry']))      
                elif 'netMHCIIpan' in program:
                    if version == '3' and 'netMHCIIpan3' not in tool_dict:
                        program = exe_paths.netMHCIIpan3
                        if program is None:
                            program = which('netMHCIIpan3')
                        else:
                            program = which(program)
                        if program is None:
                            warnings.warn(' '.join(['No valid install of', 
                                            'netMHCIIpan available']),
                                            Warning)
                            continue
                        acceptable_scoring = ['rank', 'affinity']
                        for method in scoring:
                            if method not in acceptable_scoring:
                                warnings.warn(' '.join([method, 
                                        'not compatible with netMHCIIpan']),
                                        Warning)
                                scoring.remove(method)
                        if len(scoring) > 0:
                            tool_dict['netMHCIIpan3'] = [program,
                                                            sorted(scoring)]
                    elif 'netMHCIIpan3' in tool_dict:
                        raise RuntimeError('Conflicting or repetitive installs'
                                            'of netMHCIIpan given')
                    else:
                        raise NotImplementedError(
                            ' '.join(['Neoepiscope does not support version', 
                                      version, 'of netMHCIIpan'])
                            )
                elif 'netMHCpan' in program:
                    if (('netMHCpan3' not in tool_dict and version == '3') or 
                                    ('netMHCpan4' not in tool_dict and 
                                        version == '4')):
                        if version == '3':
                            program = exe_paths.netMHCpan3
                            if program is None:
                                program = which('netMHCpan3')
                            else:
                                program = which(program)
                        elif version == '4':
                            if program is None:
                                program = which('netMHCpan4')
                            else:
                                program = which(program)
                        if program is None:
                            warnings.warn(' '.join(['No valid install of ', 
                                            'netMHCIIpan available']),
                                            Warning)
                            continue
                        if program is None:
                            warnings.warn(' '.join(['No valid install of', 
                                            'netMHCpan version', version, 
                                            'available']),  Warning)
                            continue
                        acceptable_scoring = ['rank', 'affinity']
                        for method in scoring:
                            if method not in acceptable_scoring:
                                warnings.warn(' '.join([method, 
                                            'not compatible with netMHCpan']),
                                        Warning)
                                scoring.remove(method)
                        if len(scoring) > 0:
                            if version == '3':
                                name = 'netMHCpan3'
                            elif version == '4':
                                name = 'netMHCpan4'
                            tool_dict[name] = [program, sorted(scoring)]
                    elif (('netMHCpan3' in tool_dict and version == '3') or 
                                ('netMHCpan4' in tool_dict
                                    and version == '4')):
                        raise RuntimeError('Conflicting or repetitive installs'
                                            'of netMHCpan given')
                    else:
                        raise NotImplementedError(
                            ' '.join(['Neoepiscope does not support version', 
                                      version, 'of netMHCpan'])
                            )
                else:
                    raise NotImplementedError(
                                    ' '.join(['Neoepiscope does not support', 
                                              program, 
                                              'for binding predictions'])
                                    )
        if len(tool_dict.keys()) == 0:
            warnings.warn('No binding prediction tools given, '
                          'will proceed without binding predictions', Warning)
        # Obtain VAF frequency VCF position
        VAF_pos = get_VAF_pos(args.vcf)
        # Obtain peptide sizes for kmerizing peptides
        if ',' in args.kmer_size:
            size_list = args.kmer_size.split(',')
            size_list.sort(reverse=True)
            for i in range(0, len(size_list)):
                size_list[i] = int(size_list[i])
        hla_alleles = sorted(args.alleles.split(','))
        # For retrieving genome sequence
        reference_index = bowtie_index.BowtieIndexReference(args.bowtie_index)
        # Find transcripts that haplotypes overlap 
        relevant_transcripts = process_haplotypes(args.merged_hapcut2_output, 
                                                    interval_dict)
        # Establish handling of ATGs
        if args.upstream_atgs == 'novel':
            only_novel_upstream = True
            only_downstream = False
            only_reference = False
        elif args.upstream_atgs == 'all':
            only_novel_upstream = False
            only_downstream = False
            only_reference = False
        elif args.upstream_atgs == 'none':
            only_novel_upstream = False
            only_downstream = True
            only_reference = False
        elif args.upstream_atgs == 'reference':
            only_novel_upstream = False
            only_downstream = False
            only_reference = True
        else:
            raise RuntimeError('--upstream_atgs must be one of '
                               '{"novel", "all", "none", "reference"}')
        # Establish handling of germline mutations:
        if args.germline == 'background':
            include_germline = 2
        elif args.germline == 'include':
            include_germline = 1
        elif args.germline == 'exclude':
            include_germline = 0
        else:
            raise RuntimeError('--germline must be one of '
                               '{"background", "include", "exclude"}')
        # Establish handling of somatic mutations:
        if args.somatic == 'include':
            include_somatic = 1
        elif args.somatic == 'background':
            include_somatic = 2
        elif args.somatic == 'exclude':
            include_somatic = 0
        else:
            raise RuntimeError('--somatic must be one of '
                               '{"background", "include", "exclude"}')
        # Apply mutations to transcripts and get neoepitopes
        neoepitopes = get_peptides_from_transcripts(relevant_transcripts, 
                                                    VAF_pos, cds_dict,
                                                    only_novel_upstream,
                                                    only_downstream, 
                                                    only_reference,
                                                    reference_index,
                                                    size_list, 
                                                    include_germline, 
                                                    include_somatic)
        # If neoepitopes are found, get binding scores and write results
        if len(neoepitopes.keys()) > 0:
            full_neoepitopes = gather_binding_scores(neoepitopes, tool_dict, 
                                                     hla_alleles)
            write_results(args.output_file,
                        hla_alleles, full_neoepitopes, tool_dict)
        else:
            sys.exit('No neoepitopes found')
    else:
        raise RuntimeError(''.join([args.subparser_name, 
                            ' is not a valid software mode']))

if __name__ == '__main__':
    main()