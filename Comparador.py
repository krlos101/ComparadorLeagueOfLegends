#coding: UTF_8
#Proyecto Final PAMN

import json
import sys
import requests


def main():


	SN = raw_input("\nIngresa tu Summoner Name:   ")

	Servidores_status = ["br","eune","euw","lan","las","na","oce","ru","tr"]
	Servidores_stats = ["br","eune","euw","lan","las","na","oce","ru","tr","kr"]

	Server_status(Servidores_status)

	serv_1 = raw_input("Servidor en el que juegas:    ")

	SN_2 = SN.lower()
	SN_3 = SN_2.replace(' ','')
	serv_2 = serv_1.lower()

	if serv_2 in Servidores_stats: 
		datos(SN_3,serv_2,SN)
	else:
		print("Lo sentimos no se ha encontrado el servidor indicado, terminando aplicacion")
		sys.exit(0)

	# ------------------------------------ Imprimimos los datos y estadisticas del amig@ ------------------------------------#

	SN_amigo = raw_input("\nIngresa el Summoner Name de un amigo o amiga:    ")

	serv_amigo = raw_input("Servidor en el que juega:    ")

	SN_amigo_2 = SN_amigo.lower()
	SN_amigo_3 = SN_amigo_2.replace(' ','')
	serv_amigo_2 = serv_1.lower()

	if serv_amigo_2 in Servidores_stats: 
		datos(SN_amigo_3,serv_amigo_2,SN_amigo)
	else:
		print("Lo sentimos no se ha encontrado el servidor indicado, terminando aplicacion")
		sys.exit(0)


#----------------------------------------------- Imprimimos los datos del Invocador ---------------------------------------------------#

def datos(SN_3,serv_2,SN):

	url_datos = "https://"+serv_2+".api.pvp.net/api/lol/"+serv_2+"/v1.4/summoner/by-name/"+SN+"?api_key=0744a0f0-a5c7-4b87-b513-a5ab22f09af9"
	respuesta_api_datos = requests.get(url_datos)

	riot_response = respuesta_api_datos.status_code

	if riot_response == 200:

		datos = json.loads(respuesta_api_datos.text)

		S_id = datos[SN_3]['id']
		icono = datos[SN_3]['profileIconId']
		nivel = datos[SN_3]['summonerLevel']

		if nivel == 30:

			print("\n\nDatos de invocador   ")
			print("\n\nID personal en el servidor es:   %s" %S_id)
			print("\nID del icono de invocador actual:    %d" %icono)
			print("\nNivel de invocador es %d" %nivel)

			print("\n\n")
			
			stats(serv_2, S_id)

		else:
			print("Lo sentimos tu nivel de invocador es "+str(nivel)+" debes ser nivel 30, terminando aplicación")
			sys.exit(0)

	else:
		if riot_response == 404:

			print("Summoner Name no válido o Servidor incorrecto, terminando aplicacion")
			sys.exit(0)

		else:
			if riot_response == 500:

				print("Error interno del servidor, terminanado aplcacion")
				sys.exit(0)

			else:
				if riot_response == 503:

					print("Servicio Inhabiitado, terminando aplicacion")
					sys.exit(0)


#---------------------------------------Averiguamos si los servidores están en funcionamiento-------------------------------------------#

def Server_status(Servidores_status):

	print("\n")

	for i in Servidores_status:

		url_servidores = "http://status.leagueoflegends.com/shards/"+i
		respuesta_api_servidores = requests.get(url_servidores)

		servidores = json.loads(respuesta_api_servidores.text)

		serv = servidores['services'][1]['status']

		#Lo siguiente es para dar un poco de estética a la hora de imprimir

		Imp_estado2 = "Servidor "+i.upper()+":      "+serv.upper()
		Imp_estado3 = "Servidor "+i.upper()+":     "+serv.upper()

		if len(i) == 2:
			print Imp_estado2

		if len(i) == 3:
			print Imp_estado3


	print("\n")	


#--------------------------------- Obtenemos las estadisticas del jugador de la temporada 2015 ---------------------------------------#

def stats(serv_2, S_id):

	url_stats = "https://"+serv_2+".api.pvp.net/api/lol/"+serv_2+"/v1.3/stats/by-summoner/"+str(S_id)+"/summary?season=SEASON2015&api_key=0744a0f0-a5c7-4b87-b513-a5ab22f09af9"
	respuesta_api_stats = requests.get(url_stats)

	stats = json.loads(respuesta_api_stats.text)

	unranked_1 = stats['playerStatSummaries']

	for unr_1 in unranked_1:

		Tipos = ["RankedSolo5x5","Unranked"]

		for i in Tipos:

			if unr_1['playerStatSummaryType'] == i:

				print("Estadisticas en modo de partida:    %s" %unr_1['playerStatSummaryType'])
				print("Partidas ganadas:    %d" %unr_1['wins'])	

				if i == "RankedSolo5x5":
					print("Partidas perdidas:    %d" %unr_1['losses'])

				print ("\n")
       			
				print("Mounstros Neutrales:    %d" %unr_1['aggregatedStats']['totalNeutralMinionsKilled'])
				print("\nMinions asesinados:     %d" %unr_1['aggregatedStats']['totalMinionKills'])
				print("\nMuertes de campeones:   %d" %unr_1['aggregatedStats']['totalChampionKills'])
				print("\nAsistencias totales:    %d" %unr_1['aggregatedStats']['totalAssists'])
				print("\nTorretas destruidas:    %d" %unr_1['aggregatedStats']['totalTurretsKilled'])
				print("\n\n")


if __name__ == '__main__':
	main()
