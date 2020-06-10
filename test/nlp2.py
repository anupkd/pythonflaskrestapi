import spacy
nlp = spacy.load("en_core_web_sm")
example='''
That this House notes the announcement of jan 2019 300 redundancies at the Nestlé manufacturing factories in York, Fawdon, Halifax and Girvan and that production of the Blue Riband bar will be transferred to Poland; acknowledges in the first three months of 2017 Nestlé achieved £21 billion in sales, a 0.4 per cent increase over the same period in 2016; further notes 156 of these job losses will be in York, a city that in the last six months has seen 2,000 job losses announced and has become the most inequitable city outside of the South East, and a further 110 jobs from Fawdon, Newcastle; recognises the losses come within a month of triggering Article 50, and as negotiations with the EU on the UK leaving the EU and the UK's future with the EU are commencing; further recognises the cost of importing products, including sugar, cocoa and production machinery, has risen due to the weakness of the pound and the uncertainty over the UK's future relationship with the single market and customs union; and calls on the Government to intervene and work with hon. Members, trades unions GMB and Unite and the company to avert these job losses now and prevent further job losses across Nestlé.
'''
doc = nlp(example)
print(doc.ents)
ents = list(doc.ents)
tags={}
for entity in ents:
   print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
   term=' '.join(t.orth_ for t in entity)
   if ' '.join(term) not in tags:
        tags[term]=[(entity.label, entity.label_)]
   else:
        tags[term].append((entity.label, entity.label_))


#for chunk in doc.noun_chunks:
#    print(chunk.text, chunk.root.text, chunk.root.dep_,
#            chunk.root.head.text)