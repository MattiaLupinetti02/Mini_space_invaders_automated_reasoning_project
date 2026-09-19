
time(0..n).

xcoord(X) :- maxx(M), X = 0..M.

dangerous_alien(IDAlien,X,MinY,T) :- alien(IDAlien,X,MinY,T),MinY = #min { Y : alien(_,X,Y,T) }.

possible_action(move(NewX,T),T) :- time(T), T+1 < n, cannon(X,T), xcoord(NewX), NewX != X.

possible_action(shoot(IDAlien,X,T),T) :- time(T), T < n, cannon(X,T), dangerous_alien(IDAlien,X,_,T).

1 { do(A) : possible_action(A,T) } 1 :- time(T), T < n, possible_action(_,T), not game_over(T).

move(NewX,T) :- do(move(NewX,T)).

cannon(NewX,T+1) :- move(NewX,T), T+1 < n.

shoot(IDAlien,X,T) :- do(shoot(IDAlien,X,T)).

cannon(X,T+1) :- cannon(X,T), time(T), T+1 < n, not do(move(_,T)).

alien(IDAlien,X,Y-1,T+1) :- time(T), alien(IDAlien,X,Y,T), maxy(MaxY), Y <= MaxY, not shot(IDAlien,X,T), Y-1 >= 0.

shot(IDAlien,X,T) :- shoot(IDAlien,X,T).

world_saved :- alien(_,_,Y,_), Y > 0, Aliens = #count { ID : alien(ID,_,_,_) }, Shot = #count { IDAlien : shot(IDAlien,_,_) }, Aliens == Shot.

:- not world_saved.

game_over(T) :- time(T), not alien(_,_,_,T).

finish(T) :- T = #max { T1 : shot(_,_,T1); 0 }.

#minimize { T@2 : finish(T) }.

distance(D,T) :- cannon(X1,T), cannon(X2,T+1), finish(F), T < F, D = |X2-X1|.

#minimize { D@1,T : distance(D,T) }.

#show cannon/2.
#show move/2.
#show shot/3.
#show alien/4.