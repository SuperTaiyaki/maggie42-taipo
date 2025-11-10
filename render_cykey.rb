
keys = {}
keys['a'] = 1 << 0
keys['o'] = 1 << 1
keys['t'] = 1 << 2
keys['e'] = 1 << 3
keys['it'] = 1 << 4
keys['ot'] = 1 << 5

def r(x, bit)
  if x & (1 << bit) != 0
    "[*]"
  else
    "[ ]"
  end
end

unused = 1.upto(64).filter {|i|
  !((i & (1 << 4)) != 0 && (i & (1 << 5)) != 0)
}.to_set

ARGF.each do |line|
  parts = line.strip.split(":")
  combo = 0
  parts[0].split("|").each do |c|
    c.strip!
    combo |= keys[c] if keys.has_key?(c)
  end

  line2 = 0.upto(3).map {|i| r(combo, i)}.join("")
  #line2 = 4.upto(7).map {|i| r(combo, i)}.join("")
  thumbs = [5,4].map {|i| r(combo, i)}.join(" ")
  print "#{parts[1]}: #{line2} #{thumbs}\n"

  unused.delete(combo)
end

# Basically I want to be able to query the keymap and check for gaps and whatever
# There are 6 keys available, 2^6 - 1 = 63 possible chords
# but less, because of double thumbs.
# So in thumb, out thumb, no thumb * 2^4 = 3*16 = 48 possible chords
print("Unused: \n")
unused.each { |c|
  line2 = 0.upto(3).map {|i| r(c, i)}.join("")
  #line2 = 4.upto(7).map {|i| r(combo, i)}.join("")
  thumbs = [5,4].map {|i| r(c, i)}.join(" ")
  print "#{line2} #{thumbs}\n"
}
