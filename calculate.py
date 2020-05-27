#!/usr/bin/env python3.7

from math import *

# Проверка на валидность ip адреса
def is_ip(ip: list) -> bool:
	try:
		octets = [int(octet) for octet in ip[0].split('.')]
	except:
		return 0
	if len(octets) != 4:
		return 0
	for octet in octets:
		if octet < 0 or octet > 255:
			return 0
	if len(ip) == 2 and (int(ip[1]) < 0 or int(ip[1]) > 32):
		return 0
	elif len(ip) == 2 and (int(ip[1]) >= 0 or int(ip[1]) <= 32):
		return 2
	return 1

# Получаем наш ip в качестве листа бинарных октетов из строки
def get_ip(ip_list: str) -> list:
	ip = []
	for octet in ip_list.split('.'):
		bin_numbers = str(bin(int(octet))).split('b')[1]
		ip += ['0' for k in range(0, 8 - len(bin_numbers))]
		ip += [k for k in bin_numbers]
	return ''.join(ip)

# Получаем бинарное представления числа в формате строки
def get_bin(otcet: int) -> str:
	str_otcet = ''
	str_bin= str(bin(otcet)).split('b')[1]
	for _ in range(0, 8 - len(str_bin)):
		str_otcet += '0'
	str_otcet += str_bin
	return str_otcet

# Добавляем один октет в наш массив данных сети, либо в массив бинарных представлений(зависит от option)
def add_octet(network_data: list, otcet_data: list, option: str):
	for i in range(0, len(network_data)):
		if i != 5 and i != 6:
			if option == 'bin':
				network_data[i] += get_bin(otcet_data[i])
			elif option == 'dec':
				network_data[i] += str(otcet_data[i])

# Получаем все октеты (ip, маска, инверсивная маска, ip сети, широковещательный адрес,
# ip адрес первого хоста, ip адрес последнего хоста) и записываем их в массив data, после его возвращаем
def get_all_data_octet(count: int, octet: dict) -> list:
	ip = octet['ip']
	mask = octet['mask']
	i_mask = octet['inver_mask']
	data = [ip,
			mask,
			i_mask,
			ip & mask,
			ip | i_mask,
			0,
			0,
			(ip & mask) + (0 if count != 3 else 1),
			(ip | i_mask) - (0 if count != 3 else 1)]
	return data

# Получаем индексы для дальнейшей работы в качесте листа
def get_indices(count: int) -> list:
	one_index = (0 if count == 0 else 8) * (count)
	two_index = 8 * (count + 1)
	return [one_index, two_index]

# Получаем список все масок подсети в десятичном и в ip представлении
def get_list_subnet(masks: list) -> list:
	list_subnet = []
	octets = [0, 0, 0, 0]
	for i in range(0, 33):
		octets[0] = int(masks[i][:8], 2)
		octets[1] = int(masks[i][8:16], 2)
		octets[2] = int(masks[i][16:24], 2)
		octets[3] = int(masks[i][24:32], 2)
		list_subnet.append(f'/{i} {octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}')
	return list_subnet

# Принимаем два листа куда записываем наши данные
def put_data(network_data: list, bin_data: list, ip: str, subnet_mask:str):
	inver_mask = ''
	size_host = 0
	for letter in subnet_mask:
		inver_mask += '0' if letter == '1' else '1'
	for count in range(0, 4):
		indices = get_indices(count)
		octets = get_all_data_octet(count,
				{'ip' : int(ip[indices[0]:indices[1]], 2),
				'mask' : int(subnet_mask[indices[0]:indices[1]], 2),
				'inver_mask' : int(inver_mask[indices[0]:indices[1]], 2)})
		add_octet(network_data, octets, 'dec')
		add_octet(bin_data, octets, 'bin')
		if count != 3:
			for i in range(0, 9):
				if i != 5 and i != 6:
					network_data[i] += '.'
					bin_data[i] += '.'
	for letter in inver_mask:
		if letter == '1':
			size_host += 1
	network_data[5] += str(2 ** size_host)
	network_data[6] += str((2 ** size_host) - 2)

# Функция выдает ответ в формате листа
def get_answer(ip: str, subnet_mask: str) -> list:
	answer = ''
	network_data = ['IP адрес: ',
					'Маска подсети: ',
					'Обратная маска подсети: ',
					'IP адрес сети: ',
					'Широковещательный адрес: ',
					'Количество доступных адресов в порции хоста: ',
					'Количество рабочих адресов для хостов ((2^n)-2): ',
					'IP адрес первого хоста: ',
					'IP адрес последнего хоста: ']
	bin_data = ['' for count in range(0, 9)]
	put_data(network_data, bin_data, ip, subnet_mask)
	size_separator = len(network_data[6]) + 1
	for i in range(0, len(network_data)):
		answer +=  '\n[' + str(i) + '] ' + network_data[i] + '\n'
		if i != 5 and i != 6:
			answer += bin_data[i] + '\n'
	return answer 
