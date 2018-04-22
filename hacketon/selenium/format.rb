require 'net/http'
require 'json'

$inputFile = '/tmp/mt0'
$domain = '@gmail.com'


if ARGV[0] then
  $inputFile = ARGV[0]
end

if ARGV[1] then
  $domain = ARGV[1]
end


$alpha = 'abcdefghijklmnopqrstuvwzxy'
$xalphan = 'abcdefghijklmnopqrstuvwzxy0123456789'

$la = $alpha.length - 1
$lx = $xalphan.length - 1


def output(line)

  pre = $alpha[rand(0..$la)]
  pos1 = $xalphan[rand(0..$lx)]
  pos2 = $xalphan[rand(0..$lx)]

  part =  "#{line}#{$domain}"

  line.gsub!(/[.]/,'')
  puts "#{pre}_#{line}#{pos1}_#{pos2},#{part}\n"
 
end

$lines = File.readlines($inputFile)

$last = ''
begin 
  $lines.each do |line|
    $last = line.chomp
    output($last)
  end
rescue Exception => e
  puts "Stopped at #{$last} because of : #{e}"
end

