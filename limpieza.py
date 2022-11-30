import re
import dateutil
import pandas as pd
import numpy as np
from word2number import w2n
from datetime import datetime


def extract_df(file1, file2):
    
    df1 = pd.read_csv(file1,encoding='utf-8', sep = ';')
    df2 = pd.read_csv(file2,encoding='utf-8', sep =';')
    
    return df1, df2


def fill_nans(df_ns):

    df = df_ns.fillna(method = 'ffill')
    
    # Comprobamos imprimiendo por pantalla
    # cols = df.columns
    # print(df[cols].isnull())
    
    return df

def is_numeric(lista):
    
    for elem in lista:
        if isinstance(elem, (int,float)): 
            pass
        else:
            try:
                lista[lista.index(elem)] = int(elem)
            except:
                print('No se puede',elem)
    
    return

def limpiar_orders(df_tmp):
    
    df = df_tmp.sort_values(by='order_id')
    #print(df)
    
    order_ids = list(df['order_id'])
    dates = list(df['date'])
    time = list(df['time'])
    
    # Cambiamos todos los elementos de order_ids a numérico 
    
    is_numeric(order_ids)
    
    # Limpiamos las fechas
    
    for index in range(0,len(dates)):
        
        date = dates[index]
        np_date = np.array(date)
        # Fecha vacía
        if date == '':
            final_dta = np.nan
        
        # Fecha nan  
        elif re.findall('nan',str(date),re.I):
            final_dta = np.nan
            
        # Parseamos
        else:
            try:    
                unix = float(date)
                final_dta = datetime.fromtimestamp(unix).strftime('%d-%m-%Y')
                
            except:
                
                if date[2] == '-':
                    new_datetime = dateutil.parser.parse(date, dayfirst=True)
                    final_dta = new_datetime.strftime('%d-%m-%Y')
                else:
                    try:
                        new_datetime = dateutil.parser.parse(date)
                        final_dta = new_datetime.strftime('%d-%m-%Y')
                    except:
                        print('Fallo')

   
        # Una vez calculada y actualizada la fecha válida, vamos a comprobar que sea mayor o igual a la anterior
       
        dates[index] = final_dta
        # print(index,'->',final_dta) 
    
    # No es necesario arreglar los datos de la columna de horas ya que no la utilizaremos 
    # en la predicción en ningún momento.

    
    df_clean = pd.DataFrame()
    df_clean['order_id'] = order_ids
    df_clean['date'] = dates
    
    return df_clean

def limpiar_details(df_tmp):
    
    # Ordenamos el csv según order_details_id
    
    df = df_tmp.sort_values(by='order_details_id')
    
    # Sacamos las columnas para trabajar con ellas de manera individual
    
    odetails_ids = list(df['order_details_id'])
    order_ids = list(df['order_id'])
    pizzas = list(df['pizza_id'])
    cantidades = list(df['quantity'])
    
    # Pasamos a numérico las columnas de order_details_id y order_id
    
    is_numeric(odetails_ids)
    is_numeric(order_ids)
    
    # Ahora arreglo las pizzas
    
    for index in range(0,len(pizzas)):
        
        name = pizzas[index]

        
        if name == '':
            final_nm = np.nan
            
        elif re.findall('nan',str(name),re.I):
            final_nm = np.nan
            
        else:
            
            # Si encontramos espacios , - , @ ,0 o 3 los sustituimos por sus valores correspondientes
            
            if re.findall('\s+|-+|@+|0+|3+',name):
                
                name = re.sub('\s+|-+','_',name)
                name = re.sub('@+','a',name)
                name = re.sub('0+','o',name)
                name = re.sub('3+','e',name)
            
            final_nm = name
        
        pizzas[index] = final_nm
        
        # if index < 200:
        #     print('Pizza ',index,'->',final_nm)
        
    # Vamos a arreglar la última columna , quantity
    
    for index in range(0,len(cantidades)):
        
        num = cantidades[index]
        
        if num == '' or re.findall('nan',str(num),re.I):
            final_num = np.nan
        
        else:
            try:
                final_num = int(num)
                if final_num < 0:
                    final_num = int(abs(final_num))
                
            except:
                
                final_num = int(w2n.word_to_num(str(num)))
        
        cantidades[index] = final_num  
        
        # if index < 200:
        #     print('NUM',index,'->',final_num) 
    
    
    # Creamos el df ya arreglado por completo
           
    df_clean = pd.DataFrame()
    df_clean['order_details_id'] = odetails_ids
    df_clean['order_id'] = order_ids   
    df_clean['pizza_id'] = pizzas
    df_clean['quantity'] = cantidades 
        
    return df_clean

if __name__ == '__main__':
    
    df_orders_tmp , df_odetails_tmp = extract_df('orders.csv','order_details.csv')
    
    # Limpiamos los dfs
    df_orders_cl = limpiar_orders(df_orders_tmp)
    df_odetails = limpiar_details(df_odetails_tmp)
    
    # Rellenamos los nans con bfill
    df_orders_fin = fill_nans(df_orders_cl)
    df_odetails_fin = fill_nans(df_odetails)
    
    # Creamos los csvs
    df_orders_fin.to_csv('orders_clean.csv')
    df_odetails_fin.to_csv('order_details_clean.csv')
    
    print(df_orders_fin.info())
    print(df_odetails_fin.info())
    
    
    
    
    
    # Extras - Aclaraciones de código
    
    
    # Extra 1 - Arreglar pizza_id extendido (por si falla la simplificación a una linea)
         
            
            # if re.findall('\s+',name):
            #     name = re.sub('\s+','_',name)
            #     # print('tiene espacios')
                
            # if re.findall('-+',name):
            #     name = re.sub('-+','_',name)
            #     # print('tiene guiones')
            
            # if re.findall('@+',name):
            #     name = re.sub('@+','a',name)
            #     # print('tiene arrobas')
                
            # if re.findall('0+',name):
            #     name = re.sub('0+','o',name)
            #     # print('tiene 0s')
            
            # if re.findall('3+',name):
            #     name = re.sub('3+','e',name)
            #     # print('tiene 3s')
