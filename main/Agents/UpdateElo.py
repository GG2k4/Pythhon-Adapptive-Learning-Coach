def update_elo(prevelo,score,qvec,decay):
    updatedelo = []
    for a,b,c in prevelo,qvec,score:
        updatedelo.append(a + decay * (b*c - min(a,b)))
    return updatedelo