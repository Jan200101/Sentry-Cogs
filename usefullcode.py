Get Channels the author can see
[c.name for c in server.channels if c.type == discord.ChannelType.text and author.permissions_in(c).read_messages]


Opendir
import os
os.listdir()
