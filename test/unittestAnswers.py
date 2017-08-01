'''
The Unittest file needs to have a single positive insertion, a single positive deletion, an insertion & a deletion (positive) next to each other, an insertion and a missense mutation (positive), multiple missense and an indel (positive).
-Then do all of those again, except represented by the reverse strand.
-Something that tests the 32 thing (basically make gaps) for both + and -

Tests 2 Missense next to each other and 32 thing: ENST001
1. Chromosome 1. Position 10040. Missense. 
2. Chromosome 1. Position 10080. Missense.
3. Add on another mutation (indel?)

Tests a missense mutation that affects a stop codon: ENST555 (50070-50200 +0)
1. Chromosome 1. Position 50140. Missense.

Tests 2 Indels of different types next to each other: ENST 222 (69900-70200 +0)
1. Chromosome 3. Position 70030. Insertion
2. Chromosome 3. Position 70050. Deletion
3. Chromosome 3. Position 70053. Insertion

Tests Reverse Strand missense, insertion, deletion, and GAPS: ENST333
1. Chromosome 4. Position 70000. Missense (69900-70000 -0)
2. Chromosome 4. Position 70030. Insertion (70010-70040 -1)
3. Chromosome 4. Position 70050. Deletion (70050-70180 -0)
'''
#unittestF.p 
#unittestCRF.p
#unittestCRF2.p      

chr1_dict = {
    "9990-10034": "NNNNNNNNNNNTAACCCTAACCCTAACCCTAACCCTAACCCTAAC",
    "10040-10060": "CCCTAACCCTAACCCTAACCC",
    "10070-10120": "CCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAACCCTAACCCT"
}

CCCTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
CCCTAACCCTAACCCTAACCCTAACCCTAACACCTAACCCTAACCCTAACCCCCCTAACCCTCACCCTAACCCTAACCCTAACCCTAACCCAAC
CCCTAACCCTAACCCTAACCCTAACCCTAACCCCTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
CCCTAACCCTAACCCTAACCCTAACCCTAACCCCTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAACCCTAACCCT

enst555_dict = {
    "50070-50200": "TAGCTTTTCTCTTTAG GATGATTGTTTCATTCAGTCTTATCTCTTTTAGAAAACATAGGAAAAAATTATTTAATAATAAAATTTAATTGGCAAAATGAAGGTATGGCTTATAAGAGTGTTTTCCTATTGTT"
}

chr3_dict = {
    "69900-70200": "GTTTTTAAGATGTATCTGCTTACAAATGTTAATTGCTTTATGAATCATTCCATTGTGTGATTATACCTAATTTTGTTTAGTCATTTCCCTATTGGTGTTCATTCATGCCATTTCTAATTTCTACTGTTACCCAAATGAGCACACTTACGTGTGTCTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA"
} # +0

chr4_dict = {
    "69900-70000": "CAGACTCCCCAGAGAGTTCTGTAAACAGTTGTGACCCTGACCAGCTAGTGAGACTCGCATTTATTTAGTAAAGACTAATTGACAAAGGCTTGAGTCAACAC",
    "70010-70040": "GTAATTGACATTGTGGACTTTCCAAGTAGAA",
    "70050-70180": "GGTAGATAATTATCTTTAATATTTTTTCCCACCAGCTTGATTGAATCCCTACAGTTTGAGGTCTTAGATTTGAGTCTCTAATCCATTTTGATTTAATTTTTTATATGGCCAGAGATAGGGGTCTAGTTTCG"
}

'''
    MultIndels.py Answers pt. 1:
        WT:
        CATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG T CTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGT (TAKE OUT SPACES) (REAL)
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG T CTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCC
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG TCTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG TCTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG TCTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCT
        TCATTCATGCCATTTCTAATTTCTACTGTTACCCAAATGAGCACACTTACGTGTGTCTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG TCTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAAAAATATTTATTTTCCAAAATGCCCCCAATATTGAATGTACATAGACTTCTAA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG T CTCCTTGTGA ACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC C    CAAATGAGCACACTTACGT GTG T CTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGT AAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTAT

        MT:
        CATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGT (REAL NEW)
        CATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAAATGAGCACACTTACGT G   TC CTCCTTGTGA ACTTGTGTTTTACTAGAG TATACACCTAAAAGT (REAL)
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACGTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATAT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGTGTCCTCCTTGTGAA  G   T  TGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGTGTGTCTCCTTGTGAA G   TC TGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAAGTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACGTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACGTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATAT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTGGGGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATAT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACGTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATAT
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAAGTGTCTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA 
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA
       TCATTCATGCCATTTCTAATTTCTACTGTTAC CAAT CAGT G TC CTCCTTGTGAACTTGTGTTTTACTAGAGTATACACCTAAAAGTAAGATTAATGGGTTACAGGATCTGTGAATTTTAGTTTTACAAGATATGCCAAATATCTTCCCAAACAGGACTTATCAACCTTAATTTTTATGAGTAGTATATAA
    

    MultIndels.py Answers pt. 2:
        WT:
        AAGACTAATTGACAAAGGCTTGAGTCAACA C GTAATTGACATTGTGGACTT T   CCAAGTAGAA GGTA GATAATTATCTTTAATATTTTTTCCCA (REAL)
        AAGACTAATTGACAAAGGCTTGAGTCAACA C GTAATTGACATTGTGGACTT     CCAAGTAGAA GGTA GATAATTATCTTTAATATTTTTTCCCA
                                                            AAAGCACCAAC      GGTA GATAATTATCTTTAATATTTTTTCCCACCAGC
        AAGAGTAATTGACA                             TTGTGGACTT T   CCAAGTAGAA AGCACCAAC GGTA GATAATTATCTTTAATATTTTTTCCCACCAGC
        AAGACTAATTGACAAAGGCTTGAGTCAACA C GTAATTGACATTGTGGACTT T   CCAAGTAGAA GGTA GATAATTATCTTTAATATTTTTTCCCA CCAGC
        AAGAGTAATTGACA                             TTGTGGACTT T   CCAAGTAGAA AGCACCAAC GGTAGATAATTATCTTTAATATTTTTTCCCA
        AAGACTAATTGACAAAGGCTTGAGTCAACA C GTAATTGACATTGTGGACTTGTGGACTTTCCAAGTAGAAGGTAGATAATTATCTTTAATATTTTTTCCCA


        MT:
        AAGACTAATTGACAAAGGCTTGAGTCAACA T GTAATTGACATTGTGGACTT TCG CCAAGTAGAA G    GATAATTATCTTTAATATTTTTTCCCA (REAL)
        AAGACTAATTGACAAAGGCTTGAGTCAACA T GTAATTGACATTGTGGACTT TCG CAAGTAGAA  G    GATAATTATCTTTAATATTTTTTCCCA
               ATTGACAAAGGCTTGAGTCAACA C GTAATTGACATTGTGGACTT TCG CCAAGTAGAA GGTA GATAATTATCTTTAA
      AAGACTAATTGACAAAGGCTTTAGTCAACA C GTAATTGACATTGTGGACTT TCG           G    GATAATTATCTTTAATATTTTTTCCCA
        AAGACTAATTGACAAAGGCTTTAGTCAACA C GTAATTGACATTGTGGACTT TCG           G    GATAATTATCTTTAATATTTTTTCCCA
        AAGACTAATTGACAAAGGCTTGAGTCAACA T GTAATTGACATTGTGGACTT TCG CAAGTAGAA G    GATAATTATCTTTAATATTTTTTCCCA
        AAGACTAATTGACAAAGGCTTGAGTCAACA T GTAATTGACATTGTGGACTTTTCG CAAGTAGAAGGATAATTATCTTTAATATTTTTTCCCA
    Thrown.py Answers pt. 1:
        WT:
        CCCTAACCCTAACCCTAACCCTAACCCTAACCCCTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
                                       CCCTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
        MT:
        CCCTAACCCTAACCCTAACCCTAACCCTAACACCTAACCCTAACCCTAACCCCCCTAACCCTCACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCCTAACCCTAACCCTAACCCTAACCC      CTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCCTAACCCTAACCCTAACCCTAACCC      CTAACCCTAACCCTAACCCCCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCCTAACCCTAACCCTAACCCCCCTAACCCACACCCTAACCCTAACCCTAACCCTAACCCAAC
                                       CCCTAACCCTAACCCTAACCCCCCTAACCCTCACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCCTAACCCTAACCCTAACCC          CCCTAACCCACACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCCTAACCCTAACCCTAACCCCCCTAACCCACACCCTAACCCTAACCCTAACCCTAACCCAAC
                                       CCCTAACCCTAACCCTAACCCCCCTAACCCTCACCCTAACCCTAACCCTAACCCTAACCCAAC
        CCTAACCCTAACCCTAACCCTAACCCTAACACCTAACCCTAACCCTAACCCCCCTAACCCTCACCCTAACCCTAACCCTAACCCTAACCCAAC

    Thrown.py Answers pt. 2:
        WT:
        AAGACTAATTGACAAAGGCTTGAGTCAACACGTAATTGACATTGTGGACTTTCCAAGTAGAAG
        MT:
        AAGACTAATTGACAAAGGCTTGAGTCAACATGTAATTGACATTGTGGACTTTCCAAGTAGAAG
       AAAGACTAATTGACAAAGGCTTGAGTCAACATGTAATTGACATTGTGGACTTTCCAAGTAGAA

    Thrown.py Answers pt. 3:
        WT:
        GATGATTGTTTCATTCAGTCTTATCTCTTTTAGAAAACATAGGAAAAAATTATTTAATAATAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        GATGATTGTTTCATTCAGTCTTATCTCTTTTAGAAAACATAGGAAAAAATTATTTAATAATAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        CTCTTTTAGAAAACATAGGAAAAAATTATTTAA
        CTCTTTTAGAAAACATAGGAAAAAATTATTTAATAATAAAATTTAATTGGCAAAATGAAGGTA
        MT:
        GATGATTGTTTCATTCAGTCTTATCTCTTTAAGAAAACAAAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        GATGATTGTTTCATTCAGTCTTATCTCTTTAAGAAAACAAAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        GATGATTGTTTCATTCAGTCTTATCTCTTTAAGAAAACAAAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        GATGATTGTTTCATTCAGTCTTATCTCTTTAAGAAAACAAAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        CTCTTTTAGAAAACATAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
        CTCTTTTAGAAAACATAGGAAAAAATTATTAAATAA
        CTCTTTTAGAAAACATAGGAAAAAATTATTAAATAATAAAATTTAATTGGCAAAATGAAGGTA
        CTCTTTTAGAAAACATAGGAAAAAATTATTAAAAAAAAAAATTTAATTGGCAAAATGAAGGTATGGCTT
'''