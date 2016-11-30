from sim import sim_heuristic, Game, Card

decklists = {
        'owen' : [
    (4, 'Gitaxian Probe'),
    (1, 'Apostle\'s Blessing'),
    (4, 'Mutagenic Growth'),
    (4, 'Blighted Agent'),
    (1, 'Blossoming Defense'),
    (1, 'Dismember'),
    (1, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (4, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (4, 'Groundswell'),
    (4, 'Noble Hierarch'),
    (2, 'Pendelhaven'),
    (4, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Misty Rainforest'),
    (4, 'Wooded Foothills'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Breeding Pool'),
    (2, 'Forest'),
    ],

    'stock' : [
    (1, 'Apostle\'s Blessing'),
    (4, 'Blighted Agent'),
    (4, 'Blossoming Defense'),
    (3, 'Breeding Pool'),
    (1, 'Dismember'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Forest'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (4, 'Gitaxian Probe'),
    (4, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (4, 'Groundswell'),
    (4, 'Misty Rainforest'),
    (4, 'Mutagenic Growth'),
    (4, 'Noble Hierarch'),
    (2, 'Pendelhaven'),
    (2, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (3, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Wooded Foothills')
    ],
    

    'groundswell_over_become_immense' : [
    (1, 'Apostle\'s Blessing'),
    (4, 'Blighted Agent'),
    (4, 'Blossoming Defense'),
    (3, 'Breeding Pool'),
    (1, 'Dismember'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Forest'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (4, 'Gitaxian Probe'),
    (0, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (4, 'Groundswell'),
    (4, 'Misty Rainforest'),
    (4, 'Mutagenic Growth'),
    (4, 'Noble Hierarch'),
    (2, 'Pendelhaven'),
    (2, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (3, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Wooded Foothills')
    ],
    
    'groundswell_over_probe' : [
    (1, 'Apostle\'s Blessing'),
    (4, 'Blighted Agent'),
    (4, 'Blossoming Defense'),
    (3, 'Breeding Pool'),
    (1, 'Dismember'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Forest'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (0, 'Gitaxian Probe'),
    (4, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (4, 'Groundswell'),
    (4, 'Misty Rainforest'),
    (4, 'Mutagenic Growth'),
    (4, 'Noble Hierarch'),
    (2, 'Pendelhaven'),
    (2, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (3, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Wooded Foothills')
    ],

    'groundswell_over_mutagenic' : [
    (1, 'Apostle\'s Blessing'),
    (4, 'Blighted Agent'),
    (4, 'Blossoming Defense'),
    (3, 'Breeding Pool'),
    (1, 'Dismember'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Forest'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (4, 'Gitaxian Probe'),
    (4, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (4, 'Groundswell'),
    (4, 'Misty Rainforest'),
    (0, 'Mutagenic Growth'),
    (4, 'Noble Hierarch'),
    (2, 'Pendelhaven'),
    (2, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (3, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Wooded Foothills')
    ],

    'birds_over_hiearch' : [
    (1, 'Apostle\'s Blessing'),
    (4, 'Blighted Agent'),
    (4, 'Blossoming Defense'),
    (3, 'Breeding Pool'),
    (1, 'Dismember'),
    (0, 'Dryad Arbor'), # FIXME
    (2, 'Forest'),
    (4, 'Glistener Elf'),
    (4, 'Inkmoth Nexus'),
    (4, 'Gitaxian Probe'),
    (4, 'Become Immense'),
    (4, 'Might of Old Krosa'),
    (0, 'Groundswell'),
    (4, 'Misty Rainforest'),
    (4, 'Mutagenic Growth'),
    (4, 'Birds of Paradise'),
    (2, 'Pendelhaven'),
    (2, 'Spell Pierce'),
    (1, 'Twisted Image'),
    (3, 'Vines of Vastwood'),
    (1, 'Windswept Heath'),
    (4, 'Wooded Foothills')
    ],
    }

def heuristic(game, verbose=False):
    def gitaxian_cycle():
        while game.in_hand('Gitaxian Probe'):
            game.play_spell('Gitaxian Probe')
            new_card = game.draw()
            if verbose:
                print('Gitaxian Probe -> Draw : ' + new_card[:3])

    def land_drop():
        for fetch in ['Misty Rainforest', 'Windswept Heath', 'Wooded Foothills']:
            if game.in_hand(fetch):
                game.play_spell(fetch)
                if 'Breeding Pool' in game.library:
                    game.play_from_library('Breeding Pool')
                    if verbose:
                        print(fetch + ' -> Breeding Pool')
                    return True
                if 'Forest' in game.library:
                    game.play_from_library('Forest')
                    if verbose:
                        print(fetch + ' -> Forest')
                    return True

        if game.in_hand('Breeding Pool') and not game.can_pay('U'):
            game.play('Breeding Pool')
            if verbose:
                print('Breeding Pool')
            return True

        if game.in_hand('Pendelhaven') and not game.on_board('Pendelhaven'):
            game.play('Pendelhaven')
            if verbose:
                print('Pendelhaven')
            return True

        if game.in_hand('Breeding Pool'):
            game.play('Breeding Pool')
            if verbose:
                print('Breeding Pool')
            return True

        if game.in_hand('Forest'):
            game.play('Forest')
            if verbose:
                print('Forest')
            return True

        if game.in_hand('Inkmoth Nexus'):
            game.play('Inkmoth Nexus')
            if verbose:
                print('Inkmoth Nexus')
            return True

        return False
        
    while game.mulligan > 4:
        hand = game.draw_hand()
        green_lands = len([ c for c in hand if Card(c).can_produce_mana('G') ])
        lands = len([ c for c in hand if Card(c).can_produce_mana() ])
        critters = len([ c for c in hand if Card(c).has_infect() ])

        if lands >= 2 and green_lands >= 1 and critters >= 1:
            break

    if verbose:
        print('Start')
        print(game)

    turn = 1

    infect = 0

    while True:
        if verbose:
            print('T' + str(turn))

        game.untap()
        if turn > 1:
            new_card = game.draw()
            if verbose:
                print('Draw : ' + new_card[:3])

        gitaxian_cycle()

        can_attack_nexus = False
        if game.on_board('Inkmoth Nexus'):
            can_attack_nexus = True

        drop = False
        if turn == 1 and 'Inkmoth Nexus' in game.hand and all(c == 'Inkmoth Nexus' for c in game.hand if Card(c).has_infect()):
            game.play('Inkmoth Nexus')
            drop = True
            if verbose:
                print('Inkmoth Nexus')
        else:
            drop = land_drop()

        if verbose:
            print('%sLandfall' % '' if drop else 'No ')

        critters = [ c for c in game.board if c.has_infect() and c.name != 'Inkmoth Nexus' ]

        attack = len(critters) > 0

        if not attack and can_attack_nexus and game.can_pay(['2']) and not ('Glistener Elf' in game.hand and game.can_pay(['G'])) and not ('Blighted Agent' in game.hand and game.can_pay(['1','U'])):
            nexus = None
            for c in game.board:
                if c.name == 'Inkmoth Nexus' and not c.sickness:
                    nexus = c
                    nexus.tapped = True
                    critters.append(nexus)
                    if verbose:
                        print('Activate Nexus')
                    game.optimal_pay(['1'])
                    attack = True
                    break

        pump = 0

        if attack:
            hierarchs = [ c for c in game.board if c.name == 'Noble Hierarch' ]
            if len(hierarchs) >= len(critters):
                my_base = 1 + len(hierarchs)
            else:
                my_base = len(critters)
            target_pump = max(10 - infect - my_base, 0)

            while game.in_hand('Mutagenic Growth'):
                if verbose:
                    print('Mutagenic -> +2')
                pump += 2
                game.play_spell('Mutagenic Growth')

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])


            while game.in_hand('Might of Old Krosa') and game.can_pay(['G']):
                if verbose:
                    print('Might Kr -> +4')
                pump += 4
                game.play_spell('Might of Old Krosa')
                game.optimal_pay(['G'])

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])

            if drop:
                while game.in_hand('Groundswell') and game.can_pay(['G']):
                    landfall = 4
                    if verbose:
                        print('Groundswell -> +%d' % landfall)
                    pump += landfall
                    game.play_spell('Groundswell')
                    game.optimal_pay(['G'])

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])

            while game.in_hand('Noble Hierarch') and game.can_pay(['G']):
                if verbose:
                    print('Noble Hierarch')
                game.play('Noble Hierarch')
                game.optimal_pay(['G'])

            while game.in_hand('Vines of Vastwood') and game.can_pay(['G','G']):
                if verbose:
                    print('Kicked vines -> +4')
                pump += 4
                game.play_spell('Vines of Vastwood')
                game.optimal_pay(['G','G'])

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])


            while game.in_hand('Blossoming Defense') and game.can_pay(['G']):
                if verbose:
                    print('Blossoming Defense -> +2')
                pump += 2
                game.play_spell('Blossoming Defense')
                game.optimal_pay(['G'])

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])

            while game.in_hand('Groundswell') and game.can_pay(['G']):
                landfall = 2
                if verbose:
                    print('Groundswell -> +%d' % landfall)
                pump += landfall
                game.play_spell('Groundswell')
                game.optimal_pay(['G'])

            if target_pump - pump <= 6 and game.in_hand('Become Immense') and game.can_pay(['5delve','G']):
                if verbose:
                    print('Become Imm -> +6')
                pump += 6
                game.play_spell('Become Immense')
                game.optimal_pay(['5delve','G'])

            if game.on_board('Pendelhaven'):
                c = game.get_on_board('Pendelhaven')
                if not c.tapped:
                    if verbose:
                        print('Pendelhaven boost')
                    pump += 1
                    c.tapped = True
     
            hierarchs = [ c for c in game.board if c.name == 'Noble Hierarch' ]
            if len(hierarchs) >= len(critters):
                base = 1 + len(hierarchs)
                if verbose:
                    print('Exalted : +%d' % len(hierarchs))
            else:
                base = len(critters)
                if verbose:
                    print('Attack with %d critters' % len(critters))

            if verbose:
                print('Total infect : %d+%d=%d --> %d' % (base, pump, base+pump,
                    infect+base+pump))
            infect += base+pump

            if infect >= 10:
                if verbose:
                    print(game)
                    print(game.played)
                    print('Kill')

                return turn

        can_kill_turn_2 = False
        if turn == 1 and 'Glistener Elf' in game.hand and game.can_pay(['G']):
            mut = game.hand.count('Mutagenic Growth')
            hierarch = game.hand.count('Noble Hierarch')
            p4 = game.hand.count('Groundswell') + game.hand.count('Might of Old Krosa')
            p2 = game.hand.count('Blossoming Defense')
            p6 = game.hand.count('Become Immense')
            vines = game.hand.count('Vines of Vastwood')

            one_more_green = not all(c not in ['Forest', 'Pendelhaven', 'Breeding Pool', 
                'Misty Rainforest', 'Wooded Foothills', 'Windswept Heath'] for c in game.hand)

            can_fetch = not all(c not in ['Misty Rainforest', 'Wooded Foothills', 'Windswept Heath'] for c in game.hand)

            if mut == 4 and hierarch > 0:
                can_kill_turn_2 = True

            if one_more_green:
                if mut == 3 and p2 > 0 and hierarch > 0:
                    can_kill_turn_2 = True

                if mut >= 3 and (vines > 0 or p6 > 0 or p4 > 0 or p2 > 0 or vines > 0):
                    can_kill_turn_2 = True

                if p4 >= 2 and mut >= 1:
                    can_kill_turn_2 = True

            if can_fetch and mut + game.graveyard >= 3 and p6 > 0 and 6 + mut * 2 + 1 >= 10:
                can_kill_turn_2 = True

            if can_kill_turn_2:
                if verbose:
                    print('Going for a turn 2 kill')

        if turn == 1 and not can_kill_turn_2:
            # play hierarch on turn 1
            if game.in_hand('Noble Hierarch') and game.can_pay(['G']):
                if verbose:
                    print('Noble Hierarch')
                game.play('Noble Hierarch')
                game.optimal_pay(['G'])

        while game.in_hand('Glistener Elf') and game.can_pay(['G']):
            if verbose:
                print('Glistener Elf')
            game.play('Glistener Elf')
            game.optimal_pay(['G'])

        while game.in_hand('Blighted Agent') and game.can_pay(['1','U']):
            if verbose:
                print('Blighted Agent')
            game.play('Blighted Agent')
            game.optimal_pay(['1','U'])

        while game.in_hand('Noble Hierarch') and game.can_pay(['G']):
            if verbose:
                print('Noble Hierarch')
            game.play('Noble Hierarch')
            game.optimal_pay(['G'])

        turn += 1

        if verbose:
            print(game)

        if turn > 10:
            break

    return None

if __name__ == '__main__':
    for hypothesis in decklists:
        if hypothesis != 'owen':
            continue
        print(hypothesis)
        decklist = decklists[hypothesis]

        ntries = 10000
        d = sim_heuristic(decklist, heuristic,
                heuristic_params={
                    'verbose':False
                }, ntries=ntries)

        for k in range(2,11):
            if k in d:
                print('%.2f' % (d[k]/ntries))
            else:
                print('0.0')
