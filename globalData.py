def buildArrayCards(palo):
  "build array from 1 - 13"
  cards= []
  for i in range(1, 14):
    cardRoute= "./images/handCards/"
    cards.append(cardRoute + str(i) + palo + '.png')
  return cards

treboles= buildArrayCards('c')
corazones= buildArrayCards('h')
diamantes= buildArrayCards('d')
picas= buildArrayCards('s')

allCards = treboles + corazones + diamantes + picas
#someCards = diamantes + picas

#testCards= ["./images/handCards/Ac.png", "./images/handCards/Kc.png"]