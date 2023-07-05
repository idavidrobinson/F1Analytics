TEAM_COLORS = {'alfa romeo': '#900000', 
               'alphatauri': '#2b4562', 
               'alpine': '#0090ff', 
               'aston martin': '#006f62', 
               'ferrari': '#dc0000', 
               'haas': '#ffffff', 
               'mclaren': '#ff8700', 
               'mercedes': '#00d2be', 
               'red bull': '#0600ef', 
               'williams': '#005aff'
               }

DRIVER_TEAM_COLORS = {'ALB': '#005aff', #williams
                      'ALO': '#006f62', #aston martin
                      'BOT': '#900000', #alfa romeo
                      'DEV': '#2b4562', #alphatauri
                      'GAS': '#0090ff', #alpine 
                      'HAM': '#00d2be', #mercedes
                      'HUL': '#ffffff', #haas
                      'LEC': '#dc0000', #ferrari
                      'MAG': '#ffffff', #haas
                      'MSC': '#ffffff', #haas - currently mercedes? reserve
                      'NOR': '#ff8700', #mclaren
                      'OCO': '#0090ff', #alpine 
                      'PER': '#0600ef', #red bull
                      'PIA': '#ff8700', #mclaren
                      'RIC': '#ff8700', #mclaren - currently redbull reserve 
                      'RUS': '#00d2be', #mercedes
                      'SAI': '#dc0000', #ferrari
                      'SAR': '#005aff', #williams
                      'STR': '#006f62', #aston martin   
                      'TSU': '#2b4562', #alphatauri
                      'VER': '#0600ef', #red bull 
                      'ZHO': '#900000'  #alfa romeo
                      }

BLUE_SCALE = {'very_light_blue': 'rgb(198, 219, 239)',
              'light_blue':      'rgb(107, 174, 214)',
              'blue':            'rgb( 33, 113, 181)',
              'dark_blue':       'rgb(  8,  81, 156)',
              'very_dark_blue':  'rgb(  8,  48, 107)'
}

USER_YEAR_INPUT             = int(input("Please enter the season year (for example, 2022): "))
USER_GRAND_PRIX_INPUT       = input("Please enter the Grand Prix name: ")
USER_SESSION_TYPE_INPUT     = input("Please enter the session type: ")
USER_ONE_DRIVER_CODE_INPUT  = input("Please enter the three-letter driver code: ")
USER_MULTI_DRIVER_INPUT     = input("Please enter the three-letter driver codes, separated by spaces: ").split()