
keys = {}
keys['r'] = 1 << 0
keys['s'] = 1 << 1
keys['n'] = 1 << 2
keys['i'] = 1 << 3
keys['a'] = 1 << 4
keys['o'] = 1 << 5
keys['t'] = 1 << 6
keys['e'] = 1 << 7
keys['it'] = 1 << 8
keys['ot'] = 1 << 9

def r(x, bit)
  if x & (1 << bit) != 0
    "*"
  else
    " "
  end
end

ARGF.each do |line|
  parts = line.strip.split(":")
  combo = 0
  parts[0].split("|").each do |c|
    c.strip!
    combo |= keys[c] if keys.has_key?(c)
  end

  next if !(parts[1].strip.match? /DV.[A-Z],/)

  line1 = 0.upto(3).map {|i| r(combo, i)}.join("_")
  line2 = 4.upto(7).map {|i| r(combo, i)}.join("_")
  thumbs = 8.upto(9).map {|i| r(combo, i)}.join("")
  print "#{line1}: #{parts[1]}\n#{line2}  #{thumbs}\n"

end

# Basically I want to be able to query the keymap and check for gaps and whatever
