$root = 'root.txt'

$lines = File.readlines($root)

$period = '.'
$under = '_'
$digits = '0123456789'
$alpha = 'abcdefghijklmnopqrstuvwzxy'
$xalphan = 'abcdefghijklmnopqrstuvwzxy0123456789'

$map = {'p' => $period, 'u' => $under, 'd' => $digits, 'a' => $alpha , 'x' => $xalphan}
$regex = 'xx'


def complete(test)
  $lines.each do |line|
    line = line.chomp
    line += test
    puts "#{line}\n"
  end
end


def traverse(regex)

  _top = regex.length-1

  _cur = []
  _max = []

  (0.._top).each do |i|
    _cur.push(1)
    _max.push($map[regex[i]].length)
  end

  res = ''
  (0.._top-1).each do |i|
     res += $map[regex[i]][0]
  end

  _cur[_top] = 0
  fMax = $map[regex[_top]].length - 1
  toMod = _top

  while (toMod > -1) 
     if (toMod == _top) then
        (0..fMax).each do |i|
           complete(res+$map[regex[_top]][i])
        end
       toMod -= 1
     else
       if _cur[toMod] == _max[toMod] then
          
          res = res.chop
          _cur[toMod] = 0
         toMod -= 1
       else
         if (_cur[toMod] != 0) then
           res = res.chop
         end
         res += $map[regex[toMod]][_cur[toMod]]
         _cur[toMod] += 1
         toMod += 1
       end
     end
     
  end

end

traverse($regex)
