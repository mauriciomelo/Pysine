#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pysine.py
#  
#  Copyright 2016 Erickson <erickshowplay@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import time,argparse
from urllib.request import urlopen
try:
	from bs4            import BeautifulSoup
except:
	print('''
BeautifulSoup4 não instalado
Faça a instalação do BeautifulSoup
[+] Link Download
BeautifulSoup: https://pypi.python.org/pypi/beautifulsoup4

''')	


#Adicionando mensagens na variavel
######################################################################
author   = """

											  
[+]	Author:   Erickson Douglas				  
[+]	Facebook: erickshow.mattos
[+]	Twitter:  @erickshowplay 

"""
exemplos = """
Exemplos:
./pysine --cidades Crato/CE -e Estagiario -v
./pysine -c juazeiro-do-norte/ce --empregos Vendedor,vendedor-externo --salvar vendedor.txt
./pysine -c FORTALEZA/CE,recife/pe -e web-programador,desenvolvedor,analista-desenvolvimento-de-sistemas -s ~/empregos/programador.txt"""
errorAcento ="""
[-]Erro no argumento
[-]-------------------------------------------------------
[-]não precisa colocar acento no nome da Cidade e/ou Emprego
[-]Tente novamente!
__________________________________________________________"""
errorArgumento ="""
[-]Esqueceu de algum argumento!
[-]-----------------------------
[-]Tente novamente"""
resultado="""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

{Empresadt} : {Empresadd}
{Salariodt} : {Salariodd}
{Cidadedt}  : {Cidadedd}
{Descricdt} : {Descricdd}

Link : {url}"""

#pegando as informação de cada link
######################################################################
def mostraremprego(complemento_link,salvar):
	dt,dd = list(),list()
	link  = "http://www.sine.com.br{complemento}".format(complemento=complemento_link)
	try:
		soup = BeautifulSoup(urlopen(link),"html.parser")
	except ConnectionResetError:
		time.sleep(3)
		soup = BeautifulSoup(urlopen(link),"html.parser")
	for row in soup.find("dl",{"class":"dl-horizontal"}).find_all("dt"):
		dt.append(row.get_text().rstrip().strip())
	for row in soup.find("dl",{"class":"dl-horizontal"}).find_all("dd"):
		dd.append(row.get_text().rstrip().strip())
	
	if salvar == " ":
		print(resultado.format(Empresadt=dt[0],Empresadd=dd[0],Salariodt=dt[1],Salariodd=dd[1],Cidadedt=dt[2],Cidadedd=dd[2],Descricdt=dt[3],Descricdd=dd[3],url=link))
	else:
		arq  = open(salvar)
		temp = arq.readlines()
		temp.append(resultado.format(Empresadt=dt[0],Empresadd=dd[0],Salariodt=dt[1],Salariodd=dd[1],Cidadedt=dt[2],Cidadedd=dd[2],Descricdt=dt[3],Descricdd=dd[3],url=link))
		arq = open(salvar,"w+")
		arq.writelines(temp)
		arq.close()

#buscando as vargas disponivel
##################################################################################
def procurar(cidade,estado,emprego,salvar):
	link ="http://www.sine.com.br/vagas-empregos-em-"+cidade+"-"+estado+"/"+emprego
	try:
		soup = BeautifulSoup(urlopen(link),"html.parser")
		
	except:
		time.sleep(3)
		soup = BeautifulSoup(urlopen(link),"html.parser")
	links = soup.find("div",{"class":"row jobs"}).find_all("a")
	if len(links) != 0:
		for row in links:
			mostraremprego(row.attrs["href"],salvar)
	else:
		if Verbose:
			print("[-]-----------------------")
			print("[-]Emprego não encontrado: ")
			print("[-]-----------------------")
			print(link)
	
#######################################################################
def main():
	parser = argparse.ArgumentParser(prog="./pysine",description=" Esse script foi feito para fazer busca de emprego do jeito rápido e eficaz")
	parser.add_argument("-c","--cidades", type=str, help="Pode colocar mais de uma cidade separado por vírgula, Exemplo: -c Recife/PE,Fortaleza/CE  ")
	parser.add_argument("-e","--empregos",type=str, help="Pode colocar mais de um emprego separado por vígula,  Exemplo: -s Estagiario,desenvolvedor")
	parser.add_argument("-s","--salvar", default=" ", help="Para salvar os resultados")
	parser.add_argument("-v","--verbose", action="store_true",help="Para mostrar oque está acontecendo")
	args = parser.parse_args()
	
	
	try:
		Cidades  = list(args.cidades.lower().split(","))
		Empregos = list(args.empregos.lower().split(","))
		Salvar   = args.salvar.lower()
		Verbose  = args.verbose
		if not Salvar == " ":
			arq = open(Salvar,"w+")
			arq.writelines(author) 
			arq.close()
			
		if not Cidades == "" and not Empregos == "":
			for cidade in Cidades:
				cidade,estado = cidade.split("/")[0],cidade.split("/")[1]
				for emprego in Empregos:
					procurar(cidade,estado,emprego,Salvar)
	except AttributeError:
		parser.print_help()
		print(exemplos)
		time.sleep(3)
	except UnicodeEncodeError:
		print(errorAcento)
		time.sleep(5)
		parser.print_help()
	except IndexError:
		print(exemplos)
		time.sleep(5)
		parser.print_help()
	except KeyboardInterrupt:
		print("Cancelado com sucesso")
		time.sleep(3)
		parser.print_help()
	
	
if __name__ == "__main__":
	main()