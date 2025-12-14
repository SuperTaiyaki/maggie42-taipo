#!/usr/bin/env ruby
# require 'pry'

# Things to try:
# leading E...
# ex is the main use, so change ax -> ex?
# It takes up too much space and doesn't chain to much, though. Maybe good for extra flexibility alone...
# ex pect

# Data out of the patent. Verified that this is comprehensive (but not necessarily correct)

# Generation rules: This will output the minimum set to guarantee these can all be generated

# TODO: Split this into patent versions and my version
lh = [
['A', 'A'],
['CHR', 'CHR'],
['SCTNR', 'GL'],
['ASCT', 'AG'],
['ASTNR', 'ASQ'],

['S', 'S'],
['CNR', 'CL'],
['SCWHN', 'SPY'],
['ASCW', 'ASP'],
['ASWHN', '-'],

['C', 'C'],
['TWH', 'K'],
['SCWHR', '-'],
['ASCH', '-'],
['ASWHR', '-'],

['T', 'T'],
['TWN', 'J'],
['SCWNR', 'SPL'],
['ASCN', 'ASS'],
['ASWNR', '-'],

['W', 'W'],
#['TWR', '-'], # this and STWR removed because I want more useful things for them
['SCHNR', '-'],
['ASCR', 'ASCR'],
['ASHNR', '-'],

['H', 'H'],
['THN', 'TY'],
['STWHN', 'XY'],
['ASTW', 'AX'],
['ACTWH', 'AB'],

['N', 'N'],
['THR', 'THR'],
['STWHR', '-'],
['ASTH', 'ASTH'],
['ACTWN', 'ADM'],

['R', 'R'],
['TNR', 'Q'],
['STWNR', 'SERV'],
['ASTN', '-'],
['ACTWR', 'ADDR'],

['SC', 'SC'],
['WHN', 'MY'],
['STHNR', 'STRY'],
['ASTR', '-'],
['ACTHN', 'AFF'],

['ST', 'ST'],
['WHR', '-'],
['SWHNR', '-'],
['ASWH', '-'],
['ACTHR', 'AFR'],

['SW', 'SW'],
['WNR', 'MR'],
['CTWHN', 'BY'],
['ASWN', 'ASM'],
['ACTNR', 'ACQ'],

['SH', 'SH'],
['HNR', 'LY'],
['CTWHR', 'BR'],
['ASWR', '-'],
['ACWHN', '-'],

['SN', 'SN'],
['SCTW', 'GW'],
['CTWNR', '-'],
['ASHN', 'ASY'],
['ACWHR', 'APHR'],

['SR', 'SER'],
['SCTH', 'GH'],
['CTHNR', 'FL'],
['ASHR', '-'],
['ACWNR', 'APL'],

['CT', 'D'],
['SCTN', 'GN'],
['CWHNR', 'PHL'],
['ASNR', 'ASL'],
['ACHNR', 'ACCL'],

['CW', 'P'],
['SCTR', 'GR'],
['TWHNR', 'KL'],
['ACTW', 'ADD'],
['ATWHN', 'ACKN'],

['CH', 'CH'],
['SCWH', 'SPH'],
['SCTWHN', '-'],
['ACTH', 'AF'],
['ATWHR', '-'],

['CN', 'Z'],
['SCWN', '-'],
['SCTWHR', '-'],
['ACTN', 'ADV'],
['ATWNR', '-'],

['CR', 'CR'],
['SCWR', 'SPR'],
['SCTWNR', '-'],
['ACTR', 'ADR'],
['ATHNR', 'ATHL'],

['TW', 'TW'],
['SCHN', '-'],
['SCTHNR', '-'],
['ACWH', 'APH'],
['AWHNR', '-'],

['TH', 'TH'],
['SCHR', '-'],
['SCWHNR', '-'],
['ACWN', 'AMM'],
['ASCTWH', 'ABB'],

['TN', 'V'],
['SCNR', '-'],
['STWHNR', '-'],
['ACWR', 'APR'],
['ASCTWN', 'ADJ'],

['TR', 'TR'],
['STWH', 'SK'],
['CTWHNR', 'BL'],
['ACHN', 'ACC'],
['ASCTWR', 'AGGR'],

['WH', 'WH'],
['STWN', '-'],
['SCTWHNR', '-'],
['ACHR', 'ACCR'],
['ASCTHN', 'AFT'],

['WN', 'M'],
#['STWR', 'XR'],
['AS', 'AS'],
['ACNR', '-'],
['ASCTHR', 'AFFR'],

['WR', 'WR'],
['STHN', 'STY'],
['AC', 'AC'],
['ATWH', 'AK'],
['ASCTNR', 'AGL'],

['HN', 'Y'],
['STHR', '-'],
['AT', 'AT'],
['ATWN', 'AJ'],
['ASCWHN', 'ASPHY'],

['HR', 'RH'],
['STNR', 'SQ'],
['AW', 'AW'],
['ATWR', 'ATTR'],
['ASCWHR', '-'],

['NR', 'L'],
['SWHN', '-'],
['AH', 'AH'],
['ATHN', '-'],
['ASCWNR', 'APPL'],

['SCT', 'G'],
['SWHR', '-'],
['AN', 'AN'],
['ATHR', '-'],
['ASCHNR', '-'],

['SCW', 'SP'],
['SWNR', '-'],
['AR', 'AR'],
['ATNR', 'AQ'],
['ASTWHN', '-'],

['SCH', 'SCH'],
['SHNR', 'SLY'],
['ASC', 'ASC'],
['AWHN', '-'],
['ASTWHR', '-'],

['SCN', 'SS'],
['CTWH', 'B'],
['AST', 'AST'],
['AWHR', '-'],
['ASTWNR', '-'],

['SCR', 'SCR'],
['CTWN', 'DEM'],
['ASW', '-'],
['AWNR', 'ALL'],
['ASTHNR', '-'],

['STW', 'X'],
['CTWR', 'DER'],
['ASH', 'ASH'],
['AHNR', '-'],
['ASWHNR', '-'],

['STH', '-'],
['CTHN', 'DY'],
['ASN', 'ANN'],
['ASCTW', 'AGG'],
['ACTWHN', 'ABY'],

['STN', 'SV'],
['CTHR', 'FR'],
['ASR', 'ARR'],
['ASCTH', 'AGH'],
['ACTWHR', 'ABR'],

['STR', 'STR'],
['CTNR', 'DEL'],
['ACT', 'AD'],
['ASCTN', 'AGN'],
['ACTWNR', 'ADDL'],

['SWH', '-'],
['CWHN', 'PY'],
['ACW', 'AP'],
['ASCTR', 'AGR'],
['ACTHNR', 'AFL'],

['SWN', 'SM'],
['CWHR', 'PHR'],
['ACH', 'ACH'],
['ASCWH', 'ASPH'],
['ACWHNR', '-'],

['SWR', '-'],
['CWNR', 'PL'],
['ACN', 'AZ'],
['ASCWN', 'APP'],
['ATWHNR', '-'],

['SHN', 'SY'],
['CHNR', 'CRY'],
['ACR', 'ACR'],
['ASCWR', 'APPR'],
['ASCTWHN', '-'],

['SHR', 'SHR'],
['TWHN', 'KN'],
['ATW', 'ATT'],
['ASCHN', '-'],
['ASCTWHR', 'ABBR'],

['SNR', 'SL'],
['TWHR', 'KR'],
['ATH', 'ATH'],
['ASCHR', '-'],
['ASCTWNR', 'AGGL'],

['CTW', 'DW'],
['TWNR', 'JER'],
['ATN', 'AV'],
['ASCNR', '-'],
['ASCTHNR', 'AFFL'],

['CTH', 'F'],
['THNR', 'TRY'],
['ATR', 'ATR'],
['ASTWH', 'ASK'],
['ASCWHNR', '-'],

['CTN', 'DEV'],
['WHNR', '-'],
['AWH', 'AWH'],
['ASTWN', '-'],
['ASTWHNR', '-'],

['CTR', 'DR'],
['SCTWH', '-'],
['AWN', 'AM'],
['ASTWR', '-'],
['ACTWHNR', 'ABL'],

['CWH', 'PH'],
['SCTWN', '-'],
['AWR', '-'],
['ASTHN', '-'],
['ASCTWHNR', '-'],

['CWN', 'PN'],
['SCTWR', '-'],
['AHN', 'AY'],
['ASTHR', '-'],

['CWR', 'PR'],
['SCTHN', 'GY'],
['AHR', '-'],

['CHN', 'CY'],
['SCTHR', '-'],
['ANR', 'AL'],
]

rh = [
['R', 'R'],
['RHT', 'RTH'],
['RLGH', '-'],
['RNLGC', 'LB'],
['NCHTS', 'NDS'],

['N', 'N'],
['RHS', 'WS'],
['RLGT', '-'],
['RNLGH', 'LM'],
['LGCHT', '-'],

['L', 'L'],
['RTS', 'RTS'],
['RLGS', '-'],
['RNLGT', 'KL'],
['LGCHS', '-'],

['G', 'G'],
['NLG', 'D'],
['RLCH', '-'],
['RNLGS', '-'],
['LGCTS', 'CKLES'],

['C', 'C'],
['NLC', 'SP'],
['RLCT', '-'],
['RNLCH', 'LCH'],
['LGHTS', '-'],

['H', 'H'],
['NLH', 'SH'],
['RLCS', 'RPS'],
['RNLCT', 'LP'],
['LCHTS', 'PTHS'],

['T', 'T'],
['NLT', 'ST'],
['RLHT', '-'],
['RNLCS', 'PLES'],
['GCHTS', '-'],

['S', 'S'],
['NLS', 'SS'],
['RLHS', 'WLS'],
['RNLHT', '-'],
['RNLGCH', '-'],

['RN', 'RN'],
['NGC', 'GG'],
['RLTS', '-'],
['RNLHS', 'LVES'],
['RNLGCT', '-'],

['RL', 'RL'],
['NGH', 'M'],
['RGCH', 'RF'],
['RNLTS', 'RSTS'],
['RNLGCS', 'LBS'],

['RG', 'RG'],
['NGT', 'NK'],
['RGCT', '-'],
['RNGCH', '-'],
['RNLGHT', '-'],

['RC', 'RC'],
['NGS', 'NGS'],
['RGCS', 'RBS'],
['RNGCT', '-'],
['RNLGHS', 'LMS'],

['RH', 'W'],
['NCH', 'NCH'],
['RGHT', 'WK'],
['RNGCS', '-'],
['RNLGTS', 'LKS'],

['RT', 'RT'],
['NCT', 'TION'],
['RGHS', '-'],
['RNGHT', '-'],
['RNLCHT', '-'],

['RS', 'RS'],
['NCS', 'NCES'],
['RGTS', 'RKS'],
['RNGHS', 'RMS'],
['RNLCHS', 'PHS'],

['NL', 'S'],
['NHT', 'NTH'],
['RCHT', '-'],
['RNGTS', '-'],
['RNLCTS', 'LPS'],

['NG', 'NG'],
['NHS', 'VES'],
['RCHS', 'RD'],
['RNCHT', '-'],
['RNLHTS', '-'],

['NC', 'NC'],
['NTS', 'NTS'],
['RCTS', '-'],
['RNCHS', 'WD'],
['RNGCHT', '-'],

['NH', 'V'],
['LGC', 'BL'],
['RHTS', 'RTHS'],
['RNCTS', '-'],
['RNGCHS', '-'],

['NT', 'NT'],
['LGH', 'X'],
['NLGC', '-'],
['RNHTS', 'WTHS'],
['RNGCTS', '-'],

['NS', 'NS'],
['LGT', 'LK'],
['NLGH', 'SM'],
['RLGCH', '-'],
['RNGHTS', '-'],

['LG', 'LG'],
['LGS', '-'],
['NLGT', 'SK'],
['RLGCT', '-'],
['RNCHTS', 'WDS'],

['LC', 'P'],
['LCH', 'PH'],
['NLGS', 'DS'],
['RLGCS', '-'],
['RLGCHT', '-'],

['LH', 'Z'],
['LCT', 'PT'],
['NLCH', '-'],
['RLGHT', '-'],
['RLGCHS', '-'],

['LT', 'LT'],
['LCS', 'PS'],
['NLCT', 'NST'],
['RLGHS', '-'],
['RLGCTS', '-'],

['LS', 'LS'],
['LHT', 'LTH'],
['NLCS', 'SPS'],
['RLGTS', '-'],
['RLGHTS', '-'],

['GC', 'B'],
['LHS', 'ZES'],
['NLHT', '-'],
['RLCHT', '-'],
['RLCHTS', 'RLDS'],

['GH', 'GH'],
['LTS', 'LTS'],
['NLHS', 'SHES'],
['RLCHS', 'RLD'],
['RGCHTS', '-'],

['GT', 'K'],
['GCH', 'F'],
['NLTS', 'STS'],
['RLCTS', '-'],
['NLGCHT', 'MPT'],

['GS', 'GS'],
['GCT', 'CK'],
['NGCH', 'MB'],
['RLHTS', '-'],
['NLGCHS', 'MPS'],

['CH', 'CH'],
['GCS', 'BS'],
['NGCT', 'BT'],
['RGCHT', '-'],
['NLGCTS', '-'],

['CT', 'CT'],
['GHT', 'GHT'],
['NGCS', 'GGS'],
['RGCHS', '-'],
['NLGHTS', 'DTHS'],

['CS', 'CS'],
['GHS', 'GHS'],
['NGHT', 'NGTH'],
['RGCTS', '-'],
['NLCHTS', '-'],

['HT', 'TH'],
['GTS', 'KS'],
['NGHS', 'MS'],
['RGHTS', 'WKS'],
['NGCHTS', '-'],

['HS', 'HS'],
['CHT', 'TCH'],
['NGTS', 'NKS'],
['RCHTS', 'RDS'],
['LGCHTS', '-'],

['TS', 'TS'],
['CHS', 'D'],
['NCHT', '-'],
['NLGCH', 'MP'],
['RNLGCHT', '-'],

['RNL', 'LL'],
['CTS', 'CTS'],
['NCHS', 'ND'],
['NLGCT', '-'],
['RNLGCHS', '-'],

['RNG', 'GN'],
['HTS', 'THS'],
['NCTS', '-'],
['NLGCS', '-'],
['RNLGCTS', '-'],

['RNC', '-'],
['RNLG', 'DL'],
['NHTS', 'NTHS'],
['NLGHT', 'DTH'],
['RNLGHTS', '-'],

['RNH', 'WN'],
['RNLC', 'PL'],
['LGCH', 'LF'],
['NLGHS', 'SMS'],
['RNLCHTS', 'LDS'],

['RNT', 'RNT'],
['RNLH', 'LV'],
['LGCT', 'CKL'],
['NLGTS', 'SKS'],
['RNGCHTS', '-'],

['RNS', 'RNS'],
['RNLT', 'RST'],
['LGCS', 'BLES'],
['NLCHT', '-'],
['RLGCHTS', '-'],

['RLG', '-'],
['RNLS', 'LLS'],
['LGHT', 'XT'],
['NLCHS', '-'],
['NLGCHTS', 'MPTS'],

['RLC', 'RP'],
['RNGC', '-'],
['LGHS', 'XES'],
['NLCTS', '-'],
['RNLGCHTS', '-'],

['RLH', 'WL'],
['RNGH', 'RM'],
['LGTS', '-'],
['NLHTS', '-'],
#['E', 'E'],

['RLT', '-'],
['RNGT', '-'],
['LCHT', 'PTH'],
['NGCHT', '-'],
['CTE', 'CATE'],

['RLS', 'RLS'],
['RNGS', 'GNS'],
['LCHS', 'LD'],
['NGCHS', 'MBS'],
['LGY', 'LOGY'],

['RGC', 'RB'],
['RNCH', 'RV'],
['LCTS', '-'],
['NGCTS', 'BTS'],
['GTSE', 'KES'],

['RGH', 'RGH'],
['RNCT', '-'],
['LHTS', '-'],
['NGHTS', 'NGTHS'],
['TSY', 'YS'],

['RGT', 'RK'],
['RNCS', '-'],
['GCHT', 'FT'],

['RGS', 'RGS'],
['RNHT', 'WTH'],
['GCHS', 'DG'],

['RCH', 'RCH'],
['RNHS', 'WNS'],
['GCTS', 'CKS'],

['RCT', '-'],
['RNTS', '-'],
['GHTS', 'GHTS'],

['RCS', 'RCS'],
['RLGC', '-'],
['CHTS', 'DS'],
]

# Changes memo:
# LCHS -> I typed this expecting LD
# it's only used for PHS, which is used for ~graphs - uncommon
# so exchange the two
# LGT -> I want LK
# KL is basically unused (quickly, weekly - conjugated stuff)
# so change with RNLGT
$base_rules= [		# left hand obvious
		['a', 'A'],
		['s', 'S'],
		['c', 'C'],
		['t', 'T'],
		['w', 'W'],
		['h', 'H'],
		['n', 'N'],
		['r', 'R'],

		# left hand required
		['b', 'CTWH'],
		['d', 'CT'],
		['f', 'CTH'],
		['g', 'SCT'],
		['j', 'TWN'],
		['k', 'TWH'],
		['l', 'NR'],
		['m', 'WN'],
		['p', 'CW'],
		['q', 'TNR'],
		['v', 'TN'],
		['x', 'STW'],
		['y', 'HN'],
		['z', 'CN'],


        # right hand obvious
		['r', 'r'],
		['n', 'n'],
		['l', 'l'],
		['g', 'g'],
		['c', 'c'],
		['h', 'h'],
		['t', 't'],
		['s', 's'],
		['e', 'e'],
		['y', 'y'],

		# right hand required (to be fair, you can type this with the left hand anyway, but it takes another stroke)
		['b', 'gc'],
		['d', 'nlg'],
		['d', 'chs'],
		['f', 'gch'],
		['k', 'gt'],
		['m', 'ngh'],
		['p', 'lc'],
		['v', 'nh'],
		['w', 'rh'],
		['x', 'lgh'],
        # Y is a hard key
		['z', 'lh'],
        ['s', 'nl'],  # in the patent

        # Not in the patent, just some silliness I use
        ['te', 'tdE'],
        ['ey', 'dEe'],
        ['er', 'ey'], # maybe useful?
        ['y', 'dE'],

        # Only from the wiki, but crucial
        ['qu', 'TWR'],
        ['squ', 'STWR'],
        # On top of the above, about the only combination that follows with qu?


].sort_by { |k, v| v.size * -1 }

def generate(chord)
  i = 0
  output = ""
  while i < chord.size
    rules = $base_rules.filter do |w, r|
      chord[i..].start_with? r
    end

    if rules.size > 0
      output += rules[0][0]
      i += rules[0][1].size
    else
      print "ERROR: couldn't generate #{chord[i..]} inside #{chord}\n"
      i += 1
    end
  end

  return output
end

left_sort = %w"A S C T W H N R"
right_sort = %w"r n l g c h t s e y"

lh_sorted = lh.map {|k, v| [k.upcase, v.downcase]}.sort_by { |k, v|
  val = 0
  k.each_char do |c|
    val *= 10
    val += left_sort.index(c) + 1
  end
  val
}

rh_sorted = rh.map {|k, v| [k.downcase, v.downcase]}.sort_by { |k, v|
  val = 0
  k.each_char do |c|
    val *= 10
    val += right_sort.index(c) + 1
  end
  val
}

if ARGV.size == 0
  # No arguments: Generate ruleset for jackdaw.py
  changed = true
  while changed == true
    changed = false
    lh_sorted.each do |k, v|
      next if v == "-" #|| k == v
      generated = generate(k)
      if generated != v
        #print "Diff: #{k} generates #{generated} (not #{v})\n"
        #print "'#{k.upcase.sub('A', '4')}': '#{v}',\n" if v.size > 1
        $base_rules.push([v, k])
        $base_rules.sort_by! { |k, v| v.size * -1 }

        changed = true
        break
      end
      #print("#{v} = #{k}\n")
    end
  end


  # Same with rh_sorted
  changed = true
  while changed == true
    changed = false
    rh_sorted.each do |k, v|
      next if v == "-" #|| k == v
      generated = generate(k)
      if generated != v
        #print "Diff: #{k} generates #{generated} (not #{v})\n"
        #print "'#{k.upcase.sub('A', '4')}': '#{v}',\n" if v.size > 1
        $base_rules.push([v, k])
        $base_rules.sort_by! { |k, v| v.size * -1 }

        changed = true
        break
      end
      #print("#{v} = #{k}\n")
    end
  end

  # Generate the full chord map
  # Or generate the non-natural chords for using in the circuitpy source
  output_rules = {}

  $base_rules.each do |v, k|
    #next if v == "-"# || k == v
    #generated = generate(k)
    #if generated != v
      #print "Diff: #{k} generates #{generated} (not #{v})\n"
    #print "'#{k.upcase.sub('A', '4')}': '#{v}',\n" if v.size > 1
    #end
    #print("#{v} = #{k}\n")
    k2 = k.sub('A', '4')
    if output_rules.has_key? k2[0]
      output_rules[k2[0]].push([k2, v])
    else
      output_rules[k2[0]] = [[k2, v]]
    end
  end

  print "rules = {"
  output_rules.each do |k, v|
    v.sort_by! {|x, y| x.size * -1}
    chords = v.map { |i, o|
      "('#{i}', '#{o}'),"
    }.join("")
    print "'#{k}': [#{chords}],"
  end
  print "}\n"


  #rh_sorted.each do |k, v|
  #  next if v == "-" || k == v
  #  print("#{v} = #{k}\n")
  #end

  #lh_sorted.each do |k, v|

  #end
elsif false
  # Find open combos

  lhk = %w"A S C T W H N R"
  1.upto(lhk.size) do |len|
    lhk.combination(len) do |combo|
      combo = combo.join("")
      if lh.none? {|x| x[0] == combo && x[1] != '-'}
        print "#{combo}\n"
      end
    end
  end
  rhk = %w"R N L G C H T S"
  1.upto(rhk.size) do |len|
    rhk.combination(len) do |combo|
      combo = combo.join("")
      if rh.none? {|x| x[0] == combo && x[1] != '-'}
        print "#{combo}\n"
      end
    end
  end

else
  # More useful stuff: 
  # For each position in a word, display the available chords to generate the next block
  # Useful for figuring out optimal stroke
  word = ARGV[0]
  print("#{word}\n")
  word.size.times do |i|
    lh_sorted.each do |c, g|
      if word[i..].start_with?(g)
        print(" " * i + c.upcase +  " = " + g + "\n")
      end
    end
    rh_sorted.each do |c, g|
      if word[i..].start_with?(g)
        print(" " * i + c + " = " + g + "\n")
      end
    end
  end
end
