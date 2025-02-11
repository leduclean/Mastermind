#!/usr/bin/env python3

LENGTH = 4
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus


def evaluation(arg,ref):
    LENGTH = len(arg)
    if len(arg)!= LENGTH :
        assert("quoi")
    if len(ref) != LENGTH :
        assert("quoi")
        
    nombre_bien_places=0
    nombre_mal_places=0
    deja_utilise = set([])
    for indice_arg in range(LENGTH):
        
        bien_place = False
        mal_place = False
        couleur_arg = arg[indice_arg]

        indice_temp_ref_bien = None
        indice_temp_ref_mal = None
        for indice_ref in range(LENGTH):
            if indice_ref not in deja_utilise :
        
            
                couleur_ref = ref[indice_ref]
                
                if couleur_arg == couleur_ref :
                    
                    if indice_arg == indice_ref :
                        indice_temp_ref_bien = indice_ref
                        bien_place = True
                    else : 
                        
                        indice_temp_ref_mal = indice_ref
                        mal_place = True
        
        if indice_temp_ref_bien != None :
            
            deja_utilise.add(indice_temp_ref_bien)
            indice_temp_ref_bien = None
            indice_temp_ref_mal = None
            
            
        elif indice_temp_ref_mal != None :
            
            deja_utilise.add(indice_temp_ref_mal)
            indice_temp_ref_bien = None
            indice_temp_ref_mal = None
        
        if bien_place :
            nombre_bien_places+=1
        elif mal_place:
            nombre_mal_places+=1
        
                    
    print((nombre_bien_places,nombre_mal_places))
    return(nombre_bien_places,nombre_mal_places)

"""
argument = ['E', 'G', 'Y', 'L', 'C']
ref = ['B', 'V', 'E', 'A', 'O']

evaluation(argument,ref)

argument = ['W', 'Q', 'A', 'T', 'N', 'S', 'C', 'I', 'E']
ref = ['Y', 'Q', 'H', 'G', 'D', 'T', 'J', 'J', 'I']

evaluation(argument,ref)


argument = ['Y', 'M', 'C', 'Y', 'S']
ref = ['Z', 'R', 'I', 'L', 'C']
evaluation(argument,ref)


argument = ['M', 'J', 'C', 'D', 'Y', 'O', 'T']
ref = ['T', 'M', 'K', 'Y', 'L', 'Q', 'J']
evaluation(argument,ref)

argument = ['E', 'G', 'N', 'F', 'H', 'C', 'J', 'V', 'U', 'N']
ref = ['U', 'S', 'S', 'S', 'I', 'Y', 'M', 'H', 'C', 'F']
evaluation(argument,ref)

argument = ['J', 'C', 'O', 'C', 'T', 'B']
ref = ['V', 'B', 'E', 'X', 'Q', 'G']
evaluation(argument,ref)
"""
              

        
        