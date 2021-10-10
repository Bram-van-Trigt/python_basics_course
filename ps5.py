# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, text):
        """
        :param text:
        :return: True if the phrase is in text, or false otherwise
        """
        phrase = str.lower(self.phrase)
        text = str.lower(text)
        # remove all punctuation from text string.
        for punctuation in string.punctuation:
            text = str.replace(text, punctuation, ' ')
        # split text in list of words.
        text_list = str.split(text)
        words_in_text = len(text_list)
        words_in_phrase = len(str.split(phrase))
        test_phrase = str.replace(phrase, ' ', '')
        #loop through the words in sets of phrase words to match text and phrase.
        for number in range((words_in_text - words_in_phrase + 1)):
            empty_string = ''
            test_words = str.join(empty_string, text_list[number:(number + words_in_phrase)])
            if test_words == test_phrase:
                return True
        return False

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        title = NewsStory.get_title(story)
        return PhraseTrigger.is_phrase_in(self, title)

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        description = NewsStory.get_description(story)
        return PhraseTrigger.is_phrase_in(self, description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %X")

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        # get the pubdate from NewsStory and convert time.
        pub_time = NewsStory.get_pubdate(story)
        pub_time = pub_time.replace(tzinfo=pytz.timezone("EST"))
        trigger_time = self.time.replace(tzinfo=pytz.timezone("EST"))
        if pub_time < trigger_time:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        # get the pubdate from NewsStory and convert time.
        pub_time = NewsStory.get_pubdate(story)
        pub_time = pub_time.replace(tzinfo=pytz.timezone("EST"))
        trigger_time = self.time.replace(tzinfo=pytz.timezone("EST"))
        if pub_time > trigger_time:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        if self.trigger.evaluate(story) is True:
            return False
        else:
            return True

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) and self.trigger2.evaluate(story) is True:
            return True
        else:
            return False

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) or self.trigger2.evaluate(story) is True:
            return True
        elif self.trigger1.evaluate(story) and self.trigger2.evaluate(story) is True:
            return True
        else:
            return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    # return stories

    stories_list = []
    # Loop through all NewsStory objects.
    for article in stories:
        # Check for every NewsStory if the triggers are True.
        for trigger in triggerlist:
            result = trigger.evaluate(article)
            # continue to next NewsStory on the first trigger that returns false.
            if result is True:
                last_result = True
            else:
                last_result = False
                break
        # If all triggers are True add NewsStory to stories list.
        if last_result is True:
            stories_list.append(article)
    return stories_list


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    # print(lines) # for now, print it so you see what it contains!

    # Loop through every string in lines.
    trigger_dict = {'TITLE':TitleTrigger, 'DESCRIPTION':DescriptionTrigger, 'BEFORE':BeforeTrigger, 'AFTER':AfterTrigger, 'NOT':NotTrigger, 'AND':AndTrigger, 'OR':OrTrigger}
    triggerlist = []
    triggers = {}
    for line in lines:
        # Split string based on "," in new list with strings.
        line_list = str.split(line,',')
        # If first word is 'ADD' this will create the list of triggers. Else create variables containing the trigger.
        if line_list[0] == 'ADD':
            # Loop through all trigger names and
            for number in range(len(line_list)-1):
                triggerlist.append(line_list[number+1])
        elif line_list[1] == 'AND' or line_list[1] == 'OR':
            triggers[line_list[0]] = trigger_dict.get(line_list[1])(trigger_dict.get(line_list[2]), trigger_dict.get(line_list[3]))
            print(triggers)
        elif line_list[1] == 'NOT':
            triggers[line_list[0]] = trigger_dict.get(line_list[1])(line_list[2])
        else:
            trigger_input = line_list[2]
            triggers[line_list[0]] = trigger_dict.get(line_list[1])(trigger_input)
    print(triggers)
    print(triggerlist)
    return triggerlist

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("Miami condo")
        # t2 = DescriptionTrigger("Miami")
        # t3 = DescriptionTrigger("Explosives")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            '''
            I commented out Yahoo news. 
            There has been a change to their xml lay-out causing supplied helper code to return an error.'''
            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

