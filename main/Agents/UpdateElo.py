from main.DB.elo_question import add_elo_entry

def update_elo(prevelo,score,qvec,decay):
    print(qvec)
    print(score)
    updatedelo = []
    n=len(prevelo)
    if prevelo==[0.0]*115:
        for i in range(n):
            a=qvec[i]
            b=score[i]
            updatedelo.append(a*b)
        return updatedelo
    for i in range(n):
        a=prevelo[i]
        b=qvec[i]
        c=score[i]
    # for a,b,c in prevelo,qvec,score:
        updatedelo.append(a + decay * (b*c - min(a,b)))
    # add_elo_entry(updatedelo)
    print(updatedelo)
    return updatedelo

