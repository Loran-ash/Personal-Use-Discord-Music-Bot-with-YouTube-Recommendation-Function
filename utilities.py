from collections import namedtuple


class Queue:
    def __init__(self):
        self.music = namedtuple('music', ('title', 'url', 'thumb'))
        self.current_music = self.music('', '', '')

        self.last_title_enqueued = ''
        self.queue = []

    def set_last_as_current(self):
        index = len(self.queue) - 1
        if index >= 0:
            self.current_music = self.queue[index]

    def enqueue(self, music_title, music_url, music_thumb):
        if len(self.queue) > 0:
            self.queue.append(self.music(music_title, music_url, music_thumb))
        else:
            self.queue.append(self.music(music_title, music_url, music_thumb))
            self.current_music = self.music(music_title, music_url, music_thumb)

    def dequeue(self):
        pass

    def previous(self):
        index = self.queue.index(self.current_music) - 1
        if index > 0:
            self.current_music = self.queue[index]

    def next(self):
        if self.current_music in self.queue:
            index = self.queue.index(self.current_music) + 1
            if len(self.queue) - 1 >= index:
                if self.current_music.title == self.queue[index].title and len(self.queue) - 1 > index + 1:
                    self.current_music = self.queue[index + 1]
                else:
                    self.current_music = self.queue[index]

        else:
            self.clear_queue()

    def theres_next(self):
        if self.queue.index(self.current_music) + 1 > len(self.queue) - 1:
            return False
        else:
            return True

    def clear_queue(self):
        self.queue.clear()
        self.current_music = self.music('', '', '')


class Session:
    def __init__(self, guild, channel, id=0):
        self.id = id
        self.guild = guild
        self.channel = channel
        self.q = Queue()
