#!/usr/bin/env python
import os
import sys
import subprocess

try:
    import yake
except:
    print('yake not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yake"])
    import yake

try:
    from fuzzywuzzy import fuzz
except:
    print('fuzzywuzzy not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fuzzywuzzy"])
    from fuzzywuzzy import fuzz

try:
    import spacy
except:
    print('spacy not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])
    import spacy

try:
    from rake_nltk import Rake
except:
    print('rake_nltk not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rake_nltk"])
    from rake_nltk import Rake

try:
    import pytextrank
except:
    print('pytextrank not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytextrank"])
    import pytextrank

try:
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
except:
    print('nltk not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-Levenshtein"])
except:
    print('python-Levenshtein not installed, installing now...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-Levenshtein"])

nlp = spacy.load("en_core_web_lg")
matching_ratio = 80

def extract_keywords_with_yake(text: str) -> list:
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return keywords

def extract_keywords_with_rake(text: str) -> list:
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases_with_scores()
    return keywords

def extract_keywords_with_pytextrank(text: str) -> list:
    nlp.add_pipe("textrank")
    doc = nlp(text)
    keywords = []
    for phrase in doc._.phrases:
        keywords.append((phrase.text, phrase.rank))
    return keywords

def extract_keywords_with_positionrank(text: str) -> list:
    nlp.add_pipe("positionrank")
    doc = nlp(text)
    keywords = []
    for phrase in doc._.phrases:
        keywords.append((phrase.text, phrase.rank))
    return keywords

def extract_keywords_with_topicrank(text: str) -> list:
    nlp.add_pipe("topicrank")
    doc = nlp(text)
    keywords = []
    for phrase in doc._.phrases:
        keywords.append((phrase.text, phrase.rank))
    return keywords

def fuzzy_matching(query, choices):
    best_score = 0
    best_match = None
    for choice in choices:
        score = fuzz.ratio(query, choice)
        if score > best_score:
            best_score = score
            best_match = choice
    return best_match, best_score

def fuzzy_deduplicate(lst, match_threshold=98):
    deduplicated_lst = []
    for item in lst:
        item_lower = item.lower()
        if not any(fuzz.partial_ratio(item_lower, existing_item.lower()) >= match_threshold for existing_item in deduplicated_lst):
            deduplicated_lst.append(item)
    return deduplicated_lst

text = """
Socrates: And now allow me to draw a comparison in order to
understand the effect of learning (or the lack thereof)
upon our nature. Imagine that there are people living
in a cave deep underground. The cavern has a mouth
that opens to the light above, and a passage exists
from this all the way down to the people.
 They have lived here from infancy, with their legs
and necks bound in chains. They cannot move. All they 
can do is stare directly forward, as the chains stop
them from turning their heads around. Imagine that
far above and behind them blazes a great fire. Between
this fire and the captives, a low partition is erected
along a path, something like puppeteers use to conceal
themselves during their shows.
Glaukon: I can picture it.
Socrates: Look and you will also see other people carrying
objects back and forth along the partition, things of
every kind: images of people and animals, carved
in stone and wood and other materials. Some of these
other people speak, while others remain silent.
Glaukon: A bizarre situation for some unusual captives.
Socrates: So we are! Now, tell me if you suppose it’s possible
that these captives ever saw anything of themselves or
one another, other than the shadows flitting across the
cavern wall before them?
Glaukon: Certainly not, for they are restrained, all their lives,
with their heads facing forward only.
Socrates: And that would be just as true for the objects moving
to and fro behind them?
Glaukon: Certainly.
Socrates: Now, if they could speak, would you say that these
captives would imagine that the names they gave to
the things they were able to see applied to real things?
Glaukon: It would have to be so.
Socrates: And if a sound reverberated through their cavern from
one of those others passing behind the partition, do
you suppose that the captives would think anything
but the passing shadow was what really made the
sound?
Glaukon: No, by Zeus.
Socrates: Then, undoubtedly, such captives would consider the
truth to be nothing but the shadows of the carved
objects.
Glaukon: Most certainly.
Socrates: Look again, and think about what would happen
if they were released from these chains and these
misconceptions. Imagine one of them is set free from
his shackles and immediately made to stand up and 
bend his neck around, to take steps, to gaze up toward
the fire. And all of this was painful, and the glare from
the light made him unable to see the objects that cast
the shadows he once beheld. What do you think
his reaction would be if someone informed him that
everything he had formerly known was illusion and
delusion, but that now he was a few steps closer
to reality, oriented now toward things that were
more authentic, and able to see more truly? And,
even further, if one would direct his attention to the
artificial figures passing to and fro and ask him what
their names are, would this man not be at a loss to
do so? Would he, rather, believe that the shadows he
formerly knew were more real than the objects now
being shown to him?
Glaukon: Much more real.
Socrates: Now, if he was forced to look directly at the firelight,
wouldn’t his eyes be pained? Wouldn’t he turn
away and run back to those things which he normally
perceived and understand them as more defined
and clearer than the things now being brought to his
attention?
Glaukon: That’s right.
Socrates: Now, let’s say that he is forcibly dragged up the steep
climb out of the cavern, and firmly held until finally
he stands in the light of the sun. Don’t you think that
he would be agitated and even begin to complain?
Under that light, would his eyes not be nearly
blinded, unable to discern any of those things that we
ourselves call real?
Glaukon: No, he wouldn’t see them at first.
Socrates: It would take time, I suppose, for him to get used to
seeing higher things. In the beginning, he might only
trace the shadows. Then, reflections of people and
other things in the water. Next he would come to see
the things themselves. Then he would behold the
heavenly bodies, and the heaven itself by night, seeing
the light of the stars and the moon with greater
ease than the sun and its light by day.
Glaukon: Indeed so.
Socrates: And then, I think, he would at last be able to gaze upon
the sun itself—neither as reflected in water, nor as a
phantom image in some other place, but in its own
place as it really is.
Glaukon: Undeniably.
Socrates: And now, he will begin to reason. He will find that the
sun is the source for the seasons and the years, and
governor of every visible thing, and is ultimately
the origin of everything previously known.
Glaukon: Of course. First he would see and then draw
conclusions.
Socrates: That being the case, should he remember his fellow
prisoners and their original dwelling and what
was accepted as wisdom in that setting, don’t you
imagine he would consider himself fortunate for this
transformation, and feel pity for the captives?
Glaukon: I agree.
Socrates: Now...suppose there were honors and awards among
the captives, which they granted as prizes to one
another for being the best at recognizing the various
shadows passing by or deciphering their patterns,
their order, and the relationships among them,
and therefore best at predicting what shadow would
be seen next. Do you believe that our liberated man
would be much concerned with such honors, or that
he would be jealous of those who received them? Or
that he would strive to be like those who were lauded
by the captives and enjoyed pride of place among 
them? Or would rather take Homer’s view, and “rather
wish, in earthly life, to be the humble serf of a landless
man” (Odyssey 11.489) and suffer whatever he had
to, instead of holding the views of the captives and
returning to that state of being?
Glaukon: Truly, he would rather suffer a great deal than return
to such a life.
Socrates: Well, here’s something else to consider. If such a man
would suddenly go from the sunlight to once more
descend to his original circumstances, wouldn’t his
vision by obscured by the darkness?
Glaukon: It obviously would.
Socrates: And so, let’s say he is with the captives and gets
put into the position of interpreting the wallshadows. His eyes are still adjusting to the darkness,
and it may take a while before they are. Wouldn’t he
become a laughing-stock? Wouldn’t they say, “You
have returned from your adventure up there with
ruined eyes!” Would they not say that the ascent was a
waste of time? And if they had the opportunity, do you
supposed that they might raise their hands against
him and kill this person who is trying to liberate them
to a higher plane?”
Glaukon: I’m afraid so.
Socrates: Then, my friend Glaukon, this image applies to
everything we’ve been discussing. It compares
the visible world to the underground cavern, and
the power of the sun to the fire that burned in the
cavern. You won’t misunderstand me if you connect
the captive’s ascent to be the ascent of the soul to
the intelligible world (τὸν νοητὸν τόπον). This is how I
believe, and I shared it at your wish, though heaven
knows whether it is at all true. Regardless, it appears
to me that in the realm of what can be known, the
Idea of the Good is discovered last of all, and it only
perceived with great difficulty. But, when it is seen, it
leads us directly to the finding that it is the universal
cause of all that is right and beautiful. It is the source
of visible light and the master of the same, and in the
intelligible world it is the master of truth and reason.
And whoever, in private or in public, would behave in
a sensible way, will keep this idea in focus.
Glaukon: I agree, to the extent I can manage to understand.
Socrates: Stay with me, then, for another thought. We should
not be surprised that individuals who have reached
this level might be unwilling to spend their time on
mundane affairs, for would it not be that their souls 
always feel a calling to the higher things. If our
illustration holds true, that would seem quite likely.
Glaukon: Yes, likely indeed.
Socrates: Now, would it be at all surprising for one who has
been engaged in the contemplation of holy things,
when he ventures into ways of degenerate humanity,
to appear ridiculous in his actions? What if, for
example, while his eyes were still adjusting to the
mundane gloom, he would be forced to appear in
court to hold forth about the mere shadows of justice
or the other shapes that flitted across the wall? And
to engage in debate about such concepts with
the minds of others who has never beheld the Ideal
Justice?
Glaukon: It would not surprise me the least.
Socrates: But one who has his wits about him would remember
that there are two things that pain the eyes: being
brought from darkness to light, and transitioning back
from light to darkness. Now, considering that the soul
experiences the same discomfort, this man would not
make light of another when he met with a confused
soul. He would take the time to understand if that soul
was coming from a luminous realm and his eyes were 
blinded by darkness, or whether journeying from
the darkness of ignorance into an illuminated state
had overwhelmed his eyes. One, he would consider
fortunate. He would pity the other—and if he laughed
at either, it would be less justified if he laughed at the
expense of the one who was descending from the light
above.
Glaukon: That’s a fitting way to put it.
Socrates: Of course, if I’m correct, then some of our educators
are mistaken in their view that it is possible to implant
knowledge into a person that wasn’t there originally,
like vision into the eyes of a blind man.
Glaukon: That’s what they say.
Socrates: What our message now signifies is that the ability and
means of learning is already present in the soul. As the
eye could not turn from darkness to light unless the
whole body moved, so it is that the mind can only turn
around from the world of becoming to that of Being by
a movement of the whole soul. The soul must learn, by
degrees, to endure the contemplation of Being and the
luminous realms. This is the Good, agreed?
Glaukon: Agreed.
Socrates: Therefore, of this matter itself, there must be a craft
of some kind, which would be a most efficient and
effective means of transforming the soul. It would not
be an art that gives the soul vision, but a craft at labor
under the assumption that the soul has its own innate
vision, but does not apply it properly. There must be
some kind of means for bringing this about.
Glaukon: Yes. Such a craft must exist.
"""


def main():
    yake_keywords = extract_keywords_with_yake(text)
    print('')
    print('-----------------')
    print('Yake Generated Keywords:')
    print(yake_keywords)
    

    rake_keywords = extract_keywords_with_rake(text) # Rake returns keyword first
    print('')
    print('-----------------')
    print('Rake Generated Keywords:')
    print(rake_keywords)

    pytextrank_keywords = extract_keywords_with_pytextrank(text)
    print('')
    print('-----------------')
    print('PyTextRank Generated Keywords:')
    print(pytextrank_keywords)

    positionrank_keywords = extract_keywords_with_positionrank(text)
    print('')
    print('-----------------')
    print('PositionRank Generated Keywords:')
    print(positionrank_keywords)

    topicrank_keywords = extract_keywords_with_topicrank(text)
    print('')
    print('-----------------')
    print('TopicRank Generated Keywords:')
    print(topicrank_keywords)


    yake_keywords = [keyword[0] for keyword in yake_keywords]
    rake_keywords = [keyword[1] for keyword in rake_keywords]
    pytextrank_keywords = [keyword[0] for keyword in pytextrank_keywords]
    positionrank_keywords = [keyword[0] for keyword in positionrank_keywords]
    topicrank_keywords = [keyword[0] for keyword in topicrank_keywords]

    all_keywords = [
        yake_keywords, 
        rake_keywords, 
        pytextrank_keywords, 
        positionrank_keywords, 
        topicrank_keywords
    ]

    consolidated_keywords = []

    # Iterating over each keyword from each keyword extractor
    for keywords in all_keywords:
        for keyword in keywords:
            matches = 0

            # Comparing with all other keywords
            for other_keywords in all_keywords:
                if other_keywords is not keywords: # We don't want to compare with itself
                    for other_keyword in other_keywords:
                        if fuzz.ratio(keyword, other_keyword) >= matching_ratio:
                            matches += 1
                            break # We found a match, no need to keep comparing with the rest

            if matches >= 3: # The keyword matches with at least two other keywords
                consolidated_keywords.append(keyword)

    set(consolidated_keywords)# Use set to remove duplicates

    consolidated_keywords = fuzzy_deduplicate(consolidated_keywords, match_threshold=95)
    print('')
    print('-----------------')
    print('Consolidated keywords after fuzzy deduplication: ')
    print(consolidated_keywords)

if __name__ == '__main__':
    main()