require 'socket'

s = UDPSocket.new
s.bind(nil, 5000)

20.times do |i|
  text, sender = s.recvfrom(100)
  puts "Message #{i+1}: #{text}"
end
