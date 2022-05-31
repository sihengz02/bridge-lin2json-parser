import json

data={}

for i in range(1, 74808):
    with open('raw_file/' + str(i) + '.lin', 'r') as f:
        game = f.read().splitlines()
        
        #line1 data
        viewgraph = game[0].split('|')
        assert(viewgraph[0]=='vg')
        metadata = viewgraph[1].split(',')

        vugraphFirstBoard = int(metadata[3])
        vugraphLastBoard = int(metadata[4])

        event_prefix = metadata[0] + ', '
        url = 'https://www.bridgebase.com/tools/vugraph_linfetch.php?id=' + str(i)

        #line2 data
        results = game[1].split('|')
        assert(results[0]=='rs')
        results = results[1].split(',')
        
        #line3 data
        playername = game[2].split('|')
        assert(playername[0]=='pn')
        playername = playername[1].split(',')
        
        #during-game data
        assert(game[3][0:2]=='qx')
        games = []
        string = game[3]

        for j in range(4, len(game)):
            if game[j][0:2]=='qx':
                games.append(string)
                string = game[j]
            else:
                string = string + game[j]
        games.append(string)

        for one_game in games:
            one_game = one_game.split('|')
            turn = one_game[1]
            assert(turn[0]=='o' or turn[0]=='c')
            is_open = (turn[0]=='o')
            is_close = (turn[0]=='c')
            num = (0 if is_open else 1) + (int(turn[1:]) - vugraphFirstBoard)*2
            result = results[num]

            # metadata
            key = 'id-'+str(i)+'-'+turn
            data[key] = {}
            data[key]['metadata'] = {}
            data[key]['metadata']['event'] = event_prefix + ('Open Room' if is_open else 'Close Room') + ', #' + turn[1:]
            data[key]['metadata']['source'] = url
            data[key]['metadata']['players'] = {'S': playername[0+4*is_close], 'W': playername[1+4*is_close], 'N': playername[2+4*is_close], 'E': playername[3+4*is_close]}
            
            # data
            data[key]['data'] = {}
            data[key]['data']['initial'] = {}
            data[key]['data']['bidding'] = {}
            data[key]['data']['card_play'] = []
            data[key]['data']['result'] = {}

            # data:initial
            assert(one_game[4]=='md')
            cards = one_game[5].split(',')
            dealer = int(cards[0][0])
            cards[0] = cards[0][1:]
            
            data[key]['data']['initial']['cards'] = {}
            data[key]['data']['initial']['cards']['S'] = []
            data[key]['data']['initial']['cards']['W'] = []
            data[key]['data']['initial']['cards']['N'] = []
            data[key]['data']['initial']['cards']['E'] = []

            index = ['S', 'W', 'N', 'E']
            suits = {'S', 'H', 'D', 'C'}
            for k in range(4):
                for ch in cards[k]:
                    if ch in suits:
                        suit = ch.lower()
                    else:
                        data[key]['data']['initial']['cards'][index[k]].append(suit+ch)

            for k in range(4):
                data[key]['data']['initial']['cards'][index[k]].reverse()
            
            #data:bidding
            data[key]['data']['bidding']['dealer'] = index[dealer-1]
            data[key]['data']['bidding']['sequence'] = []
            for k in range(8,len(one_game)):
                if one_game[k]=='mb':
                    k+=1
                    data[key]['data']['bidding']['sequence'].append(one_game[k].strip('!'))
                elif one_game[k]=='pc':
                    break
            
            data[key]['data']['bidding']['final'] = result[0:2]
            data[key]['data']['bidding']['declarer'] = result[2]


            #data:card_play
            one_trick=[]
            for kk in range(k,len(one_game)):
                if one_game[kk]=='pc':
                    kk+=1
                    one_trick.append(one_game[kk])
                    if len(one_trick)==4:
                        data[key]['data']['card_play'].append(one_trick)
                        one_trick=[]
            if len(one_trick)!=0:
                data[key]['data']['card_play'].append(one_trick)
                one_trick=[]
                

            #data:result
            data[key]['data']['result']['tricks_taken'] = {}
            double = 0
            for ch in result[3:]:
                if ch=='x':
                    double+=1
                else:
                    break
            
            if result[3+double]=='=':
                if result[2] in 'NS':
                    data[key]['data']['result']['tricks_taken'] = {'NS': 6+int(result[0]), 'EW': 7-int(result[0])}
                elif result[2] in 'EW':
                    data[key]['data']['result']['tricks_taken'] = {'NS': 7-int(result[0]), 'EW': 6+int(result[0])}
                else:
                    assert(0)
                data[key]['data']['result']['winner'] = ''
            
            elif result[3+double]=='+':
                if result[2]=='N' or result[2]=='S':
                    winner = 'NS'
                    data[key]['data']['result']['tricks_taken'] = {'NS': 6+int(result[0])+int(result[4+double]), 'EW': 7-int(result[0])-int(result[4+double])}
                elif result[2]=='E' or result[2]=='W':
                    winner = 'EW'
                    data[key]['data']['result']['tricks_taken'] = {'NS': 7-int(result[0])-int(result[4+double]), 'EW': 6+int(result[0])+int(result[4+double])}
                else:
                    assert(0)
                data[key]['data']['result']['winner'] = winner
                
            elif result[3+double]=='-':
                if result[2]=='N' or result[2]=='S':
                    winner = 'EW'
                    data[key]['data']['result']['tricks_taken'] = {'NS': 6+int(result[0])-int(result[4+double]), 'EW': 7-int(result[0])+int(result[4+double])}
                elif result[2]=='E' or result[2]=='W':
                    winner = 'NS'
                    data[key]['data']['result']['tricks_taken'] = {'NS': 7-int(result[0])+int(result[4+double]), 'EW': 6+int(result[0])-int(result[4+double])}
                else:
                    assert(0)
                data[key]['data']['result']['winner'] = winner

            else:
                assert(0)

            data[key]['data']['result']['double'] = double * 'x'

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)