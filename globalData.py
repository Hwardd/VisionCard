def buildArrayCards(palo):
  "build array from 1 - 13"
  cards= []
  for i in range(1, 14):
    cardRoute= "./images/handCards/"
    cards.append(cardRoute + str(i) + palo + '.png')
  return cards

treboles= buildArrayCards('t')
corazones= buildArrayCards('c')
diamantes= buildArrayCards('d')
picas= buildArrayCards('p')

allCards = treboles + corazones + diamantes + picas
someCards = diamantes + picas

testCards= ["./images/handCards/carta1.png", "./images/handCards/carta2.png"]