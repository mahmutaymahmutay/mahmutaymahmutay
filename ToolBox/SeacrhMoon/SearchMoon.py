#######################################################################################
##                                                                                   ##
##     This python tool serach a given value in Excel document and its sheets        ##
##     Author: Mahmut AY < mahmutayy@yahoo.com >                                     ##
##                                                                                   ##
##    Please run equirements.py  file first !!                                       ##
##      USAGE:  SearchMoon.py  <ExcelFilePath> <columnName> <SearchValue>            ##
#######################################################################################

import pandas as pd
import argparse
 
 
def search_column_in_excel(file_path, column_name, search_value):
    # excel sheetleri yukleyelim
    excel_data = pd.read_excel(file_path, sheet_name=None)
    # Aradıgımz sonucu sakla
    results = []
 
   
 
    for sheet_name, sheet_data in excel_data.items():
        if column_name in sheet_data.columns:  #column var mı yok m kontrol edelim
            # degeri columnd da ara
            matching_rows = sheet_data[sheet_data[column_name] == search_value]
            if not matching_rows.empty:
                #  sheet adını sonuca ekle
                matching_rows['Sheet'] = sheet_name
                results.append(matching_rows)  
 
    if results:
        final_results = pd.concat(results, ignore_index=True)
        return final_results
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no matches found
 
def main():
   
    parser = argparse.ArgumentParser(description="Search for a value in a specific column across multiple Excel sheets.")
    parser.add_argument('file_path', type=str, help="Arama yapacagimiz Excell dosya yolunu gir")
    parser.add_argument('column_name', type=str, help="NAradigimiz Column adi nedir ?")
    parser.add_argument('search_value', type=str, help="Columnda aradiğin deger nedir ?")
    args = parser.parse_args()
 
    # Perform the search
    results = search_column_in_excel(args.file_path, args.column_name, args.search_value)
    # Sonucu cıktı edelim
    if not results.empty:
 
        print("Eslesen Satirlar bUlundu:")
        print(results)
 
    else:
        print("Eşlesen bir satir BuluNamadi.")
 
if __name__ == "__main__":
     main()
