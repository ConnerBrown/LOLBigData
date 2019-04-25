import utils











def main():
    lol = utils.readTable('raw/LeagueofLegends.csv')
    i = 0
    for item in lol[1]:
        print(i , " " , item)
        i += 1

    utils.convertToNumeric(lol)
    #remove unused columns
    # 0League,1Year,2Season,3Type,4blueTeamTag,5bResult,6rResult,7redTeamTag,8gamelength,
    # 9golddiff,10goldblue,11bKills,12bTowers,13bInhibs,14bDragons,15bBarons,16bHeralds,
    # 17goldred,18rKills,19rTowers,20rInhibs,21rDragons,22rBarons,23rHeralds,24blueTop,
    # 25blueTopChamp,26goldblueTop,27blueJungle,28blueJungleChamp,29goldblueJungle,
    # 30blueMiddle,31blueMiddleChamp,32goldblueMiddle,33blueADC,34blueADCChamp,
    # 35goldblueADC,36blueSupport,37blueSupportChamp,38goldblueSupport,39blueBans,40redTop,
    # 41redTopChamp,42goldredTop,43redJungle,44redJungleChamp,45goldredJungle,46redMiddle,
    # 47redMiddleChamp,48goldredMiddle,49redADC,50redADCChamp,51goldredADC,52redSupport,
    # 53redSupportChamp,54goldredSupport,55redBans,56Address
    indexesToRemove = [0,1,2,3,4,6,7,10,17,26,29,32,35,38,39, 42,45, 48, 51, 54, 55, 56]
    lolColRemoved = utils.removeColumns(lol, indexesToRemove)
    print()
    i=0
    for item in lolColRemoved[1]:
        print(i , " " , item)
        i += 1




if __name__ == "__main__":
    main()