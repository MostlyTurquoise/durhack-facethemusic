import musicpy as mp

def encode_data(list):
    C = mp.chord('C')
    D = mp.chord('D')
    G = mp.chord('G')
    Em = mp.chord('Em')
    mp.play(C, bpm=80, wait=True)
    '''
    melody = mp.chord('C5, C5, G5, G5, A5, A5, G5, F5, F5, E5, E5, D5, D5, C5',
                    duration=[1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4],
                    interval=[1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4])

    mp.play(melody, bpm=80, wait=True)
    '''

test = [1.293782, 1.293777, 1.293799, 1.293809, 1.293774, 1.29368, 1.293424, 1.293419, 1.293466,
         1.293465, 1.293489, 1.293451]
encode_data(test)