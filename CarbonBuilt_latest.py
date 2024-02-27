import streamlit as st
import numpy as np
import matplotlib.pylab as plt
import datetime
import mysql.connector
import collections
from collections import namedtuple 
app_mode = st.sidebar.selectbox( "Choose Entity", ["Block Producer", "Block Plant","Material Supplier","Raw Material","Material Sample",
                                    "Concrete Product","Trial","TGA"])

#"Processing Conditions","Mix Design"
def connect_to_db_aws():
    conn = mysql.connector.connect(host='devcarbonbuilt.cre24agw00md.us-east-2.rds.amazonaws.com',
                user='DevCarbonBuiltDB',
                password='W9PkFnY8SUmOtIqTX40C',
                db='DevCarbonBuiltDB',
                port=3306)
    return conn

with st.sidebar:
    add_radio = st.radio(
        "Choose Operation",
        ("Add", "Edit")
    )

BlockProducerTableName = 'BlockProducer'
BlockPlantTableName = 'BlockPlant'
MaterialSupplierTableName = 'MaterialSupplier'
RawMaterialTableName = 'RawMaterial'
MaterialSampleTableName = 'MaterialSample'

if app_mode == "Block Producer":
    st.title("Block Producer")
    
    if add_radio == "Add":
        bProducerName = st.text_input('Block Producer Name')
        bProducerNumber = st.number_input(label='Number of Block Plants',min_value=1.0,value=1.0,step=1.0)
        bProducerNotes = st.text_input('Notes')
    elif add_radio == "Edit":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {BlockProducerTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        BlockProducer = namedtuple('BlockProducer',['BlockProducerName','NumberofBlockPlants','Notes'])
        if rows:
            result = {}
            bProducerIdList = list()
            column_names = cur.column_names
            for row in rows:
                result[row[0]] = BlockProducer(row[1],row[2],row[3])
                bProducerIdList.append(row[0]) 
                 
            bProducerId = st.selectbox("Block Producer Id",bProducerIdList) 
            bProducerName = st.text_input('Block Producer Name',value=result[bProducerId].BlockProducerName)
            bProducerNumber = st.number_input('Number of Block Plants',min_value=1,value=result[bProducerId].NumberofBlockPlants)
            bProducerNotes = st.text_input('Notes',value=result[bProducerId].Notes)  
        
elif app_mode == "Block Plant": 
    st.title("Block Plant")
    
    if add_radio == "Add":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {BlockProducerTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        if rows:
            bProducerIdList = {}
            for row in rows:
                bProducerIdList[row[0]]=row[1] 
            col1, col2 = st.columns(2)
            with col1:
                bProducerID = st.selectbox("Block Producer Id",bProducerIdList)
            with col2:
                bProducerName = st.text_input('Block Producer Name',value=bProducerIdList[bProducerID])
        
        bPlantRegion = st.text_input('Block Plant Region')
        bPlantAddress = st.text_input('Block Plants Address') 
        bcanUseRailRoad = st.selectbox("Can Use Railroad",("Yes","No","May Be"))
        bProductOffering = st.text_input("Product Offering & Production Volume")
        bPowerCo2Src = st.text_input("Power / CO2 source")
        #bMaterailLandedCost = st.number_input(label='Material Landed Cost',min_value=1.0,max_value=100.0, value=1.0,step=1.0)
        st.caption('Average Monthly Temperature')
        Temp1, Temp2, Temp3 = st.columns(3)
        with Temp1:
            bPlantTempJan = st.number_input(label='January',min_value=1.0,max_value=100.0, value=1.0,step=1.0)
            bPlantTempApril = st.number_input(label='April',min_value=1.0,value=1.0,step=1.0)
            bPlantTempJully = st.number_input(label='July',min_value=1.0,value=1.0,step=1.0)
            bPlantTempOct = st.number_input(label='October',min_value=1.0,value=1.0,step=1.0)
        with Temp2:
            bPlantTempFeb = st.number_input(label='February',min_value=1.0,value=1.0,step=1.0)
            bPlantTempMay = st.number_input(label='May',min_value=1.0,value=1.0,step=1.0) 
            bPlantTempAugust = st.number_input(label='August',min_value=1.0,value=1.0,step=1.0)
            bPlantTempNov = st.number_input(label='November',min_value=1.0,value=1.0,step=1.0)
        with Temp3:
            bPlantTempMarch = st.number_input(label='March',min_value=1.0,value=1.0,step=1.0)
            bPlantTempJune = st.number_input(label='June',min_value=1.0,value=1.0,step=1.0)
            bPlantTempSep = st.number_input(label='September',min_value=1.0,value=1.0,step=1.0) 
            bPlantTempDec = st.number_input(label='December',min_value=1.0,value=1.0,step=1.0)
    elif add_radio == "Edit":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {BlockPlantTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        BlockPlant = namedtuple(BlockPlantTableName,['bProducerID','bRegion','bAddress','CanUseRailroad',
                                                'ProductOffer_ProductionVolume', 'Power_CO2_source', 'Jan_Month_Avg_Temp', 'Feb_Month_Avg_Temp', 'Mar_Month_Avg_Temp', 'April_Month_Avg_Temp', 'May_Month__Avg_Temp', 'June_Month_Avg_Temp', 'July_Month_Avg_Temp',  'August_Month_Avg_Temp', 'Sep_Month_Avg_Temp', 'Oct_Month_Avg_Temp', 'Nov_Month_Avg_Temp', 'Dec_Month_Avg_Temp'])
        if rows:
            result = {}
            bBlocklPlantList = list()
            for row in rows:
                result[row[0]] = BlockPlant(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13],row[14],row[15],row[16],row[17],row[18])
                bBlocklPlantList.append(row[0])
                                                     
            bPlantID = st.selectbox("Block Plant Id",bBlocklPlantList)
                                                     
            select_all_rows_query = f'SELECT * FROM {BlockProducerTableName}'
            cur.execute(select_all_rows_query)
            rows = cur.fetchall()
            if rows:
                bProducerIdList = {}
                for row in rows:
                    bProducerIdList[row[0]]=row[1] 
                col1, col2 = st.columns(2)
                with col1:
                    bProducerID = st.selectbox("Block Producer Id",bProducerIdList)
                with col2:
                    bProducerName = st.text_input('Block Producer Name',value=bProducerIdList[bProducerID])

            bPlantRegion = st.text_input('Block Plant Region',value=result[bPlantID].bRegion)
            bPlantAddress = st.text_input('Block Plants Address',value=result[bPlantID].bAddress) 
            bcanUseRailRoad = st.selectbox("Can Use Railroad",("Yes","No","May Be"))
            bProductOffering = st.text_input("Product Offering & Production Volume",value=result[bPlantID].ProductOffer_ProductionVolume)
            bPowerCo2Src = st.text_input("Power / CO2 source",value=result[bPlantID].Power_CO2_source)
        #bMaterailLandedCost = st.number_input(label='Material Landed Cost',min_value=1.0,max_value=100.0, value=1.0,step=1.0)
            st.caption('Average Monthly Temperature')
            Temp1, Temp2, Temp3 = st.columns(3)
            with Temp1:
                bPlantTempJan = st.number_input(label='January',min_value=1.0,max_value=100.0, value=result[bPlantID].Jan_Month_Avg_Temp, step=1.0)
                bPlantTempApril = st.number_input(label='April',min_value=1.0,value=result[bPlantID].April_Month_Avg_Temp,step=1.0)
                bPlantTempJully = st.number_input(label='July',min_value=1.0,value=result[bPlantID].July_Month_Avg_Temp,step=1.0)
                bPlantTempOct = st.number_input(label='October',min_value=1.0,value=result[bPlantID].Oct_Month_Avg_Temp,step=1.0)
            with Temp2:
                bPlantTempFeb = st.number_input(label='February',min_value=1.0,value=result[bPlantID].Feb_Month_Avg_Temp,step=1.0)
                bPlantTempMay = st.number_input(label='May',min_value=1.0,value=result[bPlantID].May_Month__Avg_Temp,step=1.0) 
                bPlantTempAugust = st.number_input(label='August',min_value=1.0,value=result[bPlantID].August_Month_Avg_Temp,step=1.0)
                bPlantTempNov = st.number_input(label='November',min_value=1.0,value=result[bPlantID].Nov_Month_Avg_Temp,step=1.0)
            with Temp3:
                bPlantTempMarch = st.number_input(label='March',min_value=1.0,value=result[bPlantID].Mar_Month_Avg_Temp,step=1.0)
                bPlantTempJune = st.number_input(label='June',min_value=1.0,value=result[bPlantID].June_Month_Avg_Temp,step=1.0)
                bPlantTempSep = st.number_input(label='September',min_value=1.0,value=result[bPlantID].Sep_Month_Avg_Temp,step=1.0) 
                bPlantTempDec = st.number_input(label='December',min_value=1.0,value=result[bPlantID].Dec_Month_Avg_Temp,step=1.0)

elif app_mode == "Material Supplier": 
    st.title("Material Supplier")
    if add_radio == "Add":
        MaterailSupplierName = st.text_input('Material Supplier Name')
    elif add_radio == "Edit":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {MaterialSupplierTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        if rows:
            bMaterailSupplierList = {}
            for row in rows:
                bMaterailSupplierList[row[0]]=row[1] 
            MaterailSupplierId = st.selectbox("Material Supplier Id",bMaterailSupplierList)
            MaterailSupplierName = st.text_input('Material Supplier Name',value=bMaterailSupplierList[MaterailSupplierId])
        
elif app_mode == "Raw Material": 
    st.title("Raw Material")
    if add_radio == "Add":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {MaterialSupplierTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        if rows:
            bMaterailSupplierList = {}
            for row in rows:
                bMaterailSupplierList[row[0]]=row[1] 
            col1, col2 = st.columns(2)
            with col1:
                MaterailSupplierId = st.selectbox("Material Supplier Id",bMaterailSupplierList)
            with col2:
                MaterailSupplierName = st.text_input('Material Supplier Name',value=bMaterailSupplierList[MaterailSupplierId])
            
        MaterialType = st.selectbox("Material Type",("Cement","Fly ash (FA)"," Lime residue (LR)","Lime kiln dust (LKD)","Gypsum","Pozzolan","Slag cement","Grate ash", "Cement kiln dust (CKD)" ,"Virgin hydrated lime", "Limestone powder", "Other lime sources","Fine aggregate (Sand)", "Intermediate aggregate", "Coarse aggregate", "Lightweight aggregate (LWA)", "Admixture"))
        Address = st.text_input('Raw Material Address')
        Density = st.number_input(label='Density',min_value=1.0,value=1.0,step=1.0)
        Sieve_4 = st.number_input(label='Sieve #4',min_value=1.0,value=1.0,step=1.0)
        Sieve_30 = st.number_input(label='Sieve #30',min_value=1.0,value=1.0,step=1.0)
        Sieve_100 = st.number_input(label='Sieve #100',min_value=1.0,value=1.0,step=1.0)
        Sieve_325 = st.number_input(label='Sieve #325',min_value=1.0,value=1.0,step=1.0)
        Water_Absorption = st.number_input(label='Water Absorption',min_value=1.0,value=1.0,step=1.0)
        Finenessmodulus = st.number_input(label='Fineness modulus',min_value=1.0,value=1.0,step=1.0)
        SiO2 = st.number_input(label='Silicon Dioxide (SiO2)',min_value=1.0,value=1.0,step=1.0)
        Al2O3 = st.number_input(label='Aluminum Oxide (Al2O3)',min_value=1.0,value=1.0,step=1.0)
        Fe2O3 = st.number_input(label='Ferric Oxide (Fe2O3)',min_value=1.0,value=1.0,step=1.0)
        CaO = st.number_input(label='Calcium Oxide (Total Lime) (CaO)',min_value=1.0,value=1.0,step=1.0)
        FreeLime = st.number_input(label='Free Lime',min_value=1.0,value=1.0,step=1.0)
        MgO = st.number_input(label='Magnesium Oxide (MgO)',min_value=1.0,value=1.0,step=1.0)
        SO3 = st.number_input(label='Sulfur Trioxide (SO3)',min_value=1.0,value=1.0,step=1.0)
        Na2O = st.number_input(label='Sodium Oxide (Na2O)',min_value=1.0,value=1.0,step=1.0)
        K2O = st.number_input(label='Potassium Oxide (K2O)',min_value=1.0,value=1.0,step=1.0)
        CaCO3 = st.number_input(label='Calcium carbonate (CaCO3)',min_value=1.0,value=1.0,step=1.0)
        Fluorine = st.number_input(label='Fluorine (F)',min_value=1.0,value=1.0,step=1.0)
        Chloride = st.number_input(label='Chloride (Cl)',min_value=1.0,value=1.0,step=1.0)
        TotalAlkalis = st.number_input(label='Total Alkalis',min_value=1.0,value=1.0,step=1.0)
        AvailableAlkalis = st.number_input(label='Available Alkalis (Na2O equivalent)',min_value=1.0,value=1.0,step=1.0)
        LossonIgnition = st.number_input(label='Loss on Ignition',min_value=1.0,value=1.0,step=1.0)
        Moisturecontent = st.number_input(label='Moisture content',min_value=1.0,value=1.0,step=1.0)
        Insolubleresidue = st.number_input(label='Insoluble residue',min_value=1.0,value=1.0,step=1.0)
        Freewater = st.number_input(label='Free water',min_value=1.0,value=1.0,step=1.0)
        ChemicalPlaceholder1 = st.number_input(label='Chemical Placeholder 1',min_value=1.0,value=1.0,step=1.0)
        ChemicalPlaceholder2 =st.number_input(label='Chemical Placeholder 2',min_value=1.0,value=1.0,step=1.0)
        ChemicalPlaceholder3 =st.number_input(label='Chemical Placeholder 3',min_value=1.0,value=1.0,step=1.0)
        ChemicalPlaceholder4 =st.number_input(label='Chemical Placeholder 4',min_value=1.0,value=1.0,step=1.0)
        Blainefineness = st.number_input(label='Blaine fineness',min_value=1.0,value=1.0,step=1.0)
        SAI7 = st.number_input(label='Strength Activity Index (SAI) at 7 day',min_value=1.0,value=1.0,step=1.0)
        SAI28 = st.number_input(label='Strength Activity Index (SAI) at 28 day',min_value=1.0,value=1.0,step=1.0)
        Limereactivity = st.number_input(label='Lime reactivity',min_value=1.0,value=1.0,step=1.0)
        Waterrequirement = st.number_input(label='Water requirement',min_value=1.0,value=1.0,step=1.0)
        Autoclaveexpansion = st.number_input(label='Autoclave expansion',min_value=1.0,value=1.0,step=1.0)
        Aircontent = st.number_input(label='Air content',min_value=1.0,value=1.0,step=1.0)
        color = st.text_input('Color')
        PhysicalPlaceholder1 = st.number_input(label='Physical Placeholder 1',min_value=1.0,value=1.0,step=1.0)
        PhysicalPlaceholder2 = st.number_input(label='Physical Placeholder 2',min_value=1.0,value=1.0,step=1.0)
        PhysicalPlaceholder3 = st.number_input(label='Physical Placeholder 3',min_value=1.0,value=1.0,step=1.0)
        PhysicalPlaceholder4 = st.number_input(label='Physical Placeholder 4',min_value=1.0,value=1.0,step=1.0)
        uploaded_file = st.file_uploader("PSD Table & Graph")
        if uploaded_file is not None:
            st.image(uploaded_file, caption=uploaded_file.name)
    elif add_radio == "Edit":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {RawMaterialTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        RawMaterial = namedtuple(RawMaterialTableName,['mattSupplierID','MaterialType', 'AddressSource','Density', 'Sieve4', 'Sieve30', 'Sieve100', 'Sieve325', 'WaterAbsorption', 'Finenessmodulus', 'SiO2', 'Al2O3', 'Fe2O3', 'CaO', 'FreeLime', 'MgO', 'SO3', 'Na2O', 'K2O', 'CaCO3', 'Fluorine', 'Chloride', 'TotalAlkalis', 'AvailableAlkalis', 'LossonIgnition', 'Moisturecontent', 'Insolubleresidue', 'Freewater', 'ChemicalPlaceholder1','ChemicalPlaceholder2','ChemicalPlaceholder3','ChemicalPlaceholder4','Blainefineness','SAIat7','SAIat28','Limereactivity','Waterrequirement','Autoclaveexpansion','Aircontent','color','PhysicalPlaceholder1','PhysicalPlaceholder2','PhysicalPlaceholder3','PhysicalPlaceholder4','PSDTableandGraph'])
        if rows:
            result = {}
            RawMaterialIdList = list()
            for row in rows:
                result[row[0]] = RawMaterial(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],row[45])
                RawMaterialIdList.append(row[0])
              
            rawMaterailID = st.selectbox("Raw Materail Id",RawMaterialIdList) 
            select_all_rows_query = f'SELECT * FROM {MaterialSupplierTableName}'
            cur.execute(select_all_rows_query)
            rows = cur.fetchall()
            if rows:
                bMaterailSupplierList = {}
                for row in rows:
                    bMaterailSupplierList[row[0]]=row[1]
                
                col1, col2 = st.columns(2)
                with col1:
                    MaterailSupplierId = st.selectbox("Material Supplier Id",bMaterailSupplierList)
                with col2:
                    MaterailSupplierName = st.text_input('Material Supplier Name',value=bMaterailSupplierList[MaterailSupplierId])     
                                              
            Density = st.number_input(label='Density',min_value=1.0,value=result[rawMaterailID].Density,step=1.0)
            MaterialType = st.selectbox("Material Type",("M1","M2","M3"))
            Address = st.text_input('Raw Material Address',value= result[rawMaterailID].AddressSource)
            Sieve_4 = st.number_input(label='Sieve #4',min_value=1.0,value=result[rawMaterailID].Sieve4,step=1.0)
            Sieve_30 = st.number_input(label='Sieve #30',min_value=1.0,value=result[rawMaterailID].Sieve30,step=1.0)
            Sieve_100 = st.number_input(label='Sieve #100',min_value=1.0,value=result[rawMaterailID].Sieve100,step=1.0)
            Sieve_325 = st.number_input(label='Sieve #325',min_value=1.0,value=result[rawMaterailID].Sieve325,step=1.0)
            Water_Absorption = st.number_input(label='Water Absorption',min_value=1.0,value=result[rawMaterailID].WaterAbsorption,step=1.0)
            Finenessmodulus = st.number_input(label='Fineness modulus',min_value=1.0,value=result[rawMaterailID].Finenessmodulus,step=1.0)
            SiO2 = st.number_input(label='Silicon Dioxide (SiO2)',min_value=1.0,value=result[rawMaterailID].SiO2,step=1.0)
            Al2O3 = st.number_input(label='Aluminum Oxide (Al2O3)',min_value=1.0,value=result[rawMaterailID].Al2O3,step=1.0)
            Fe2O3 = st.number_input(label='Ferric Oxide (Fe2O3)',min_value=1.0,value=result[rawMaterailID].Fe2O3,step=1.0)
            CaO = st.number_input(label='Calcium Oxide (Total Lime) (CaO)',min_value=1.0,value=result[rawMaterailID].CaO,step=1.0)
            FreeLime = st.number_input(label='Free Lime',min_value=1.0,value=result[rawMaterailID].FreeLime,step=1.0)
            MgO = st.number_input(label='Magnesium Oxide (MgO)',min_value=1.0,value=result[rawMaterailID].MgO,step=1.0)
            SO3 = st.number_input(label='Sulfur Trioxide (SO3)',min_value=1.0,value=result[rawMaterailID].SO3,step=1.0)
            Na2O = st.number_input(label='Sodium Oxide (Na2O)',min_value=1.0,value=result[rawMaterailID].Na2O,step=1.0)
            K2O = st.number_input(label='Potassium Oxide (K2O)',min_value=1.0,value=result[rawMaterailID].K2O,step=1.0)
            CaCO3 = st.number_input(label='Calcium carbonate (CaCO3)',min_value=1.0,value=result[rawMaterailID].CaCO3,step=1.0)
            Fluorine = st.number_input(label='Fluorine (F)',min_value=1.0,value=result[rawMaterailID].Fluorine,step=1.0)
            Chloride = st.number_input(label='Chloride (Cl)',min_value=1.0,value=result[rawMaterailID].Chloride,step=1.0)
            TotalAlkalis = st.number_input(label='Total Alkalis',min_value=1.0,value=result[rawMaterailID].TotalAlkalis,step=1.0)
            AvailableAlkalis = st.number_input(label='Available Alkalis (Na2O equivalent)',min_value=1.0,value=result[rawMaterailID].AvailableAlkalis,step=1.0)
            LossonIgnition = st.number_input(label='Loss on Ignition',min_value=1.0,value=result[rawMaterailID].LossonIgnition,step=1.0)
            Moisturecontent = st.number_input(label='Moisture content',min_value=1.0,value=result[rawMaterailID].Moisturecontent,step=1.0)
            Insolubleresidue = st.number_input(label='Insoluble residue',min_value=1.0,value=result[rawMaterailID].Insolubleresidue,step=1.0)
            Freewater = st.number_input(label='Free water',min_value=1.0,value=result[rawMaterailID].Freewater,step=1.0)
            ChemicalPlaceholder1 = st.number_input(label='Chemical Placeholder 1',min_value=1.0,value=result[rawMaterailID].ChemicalPlaceholder1,step=1.0)
            ChemicalPlaceholder2 =st.number_input(label='Chemical Placeholder 2',min_value=1.0,value=result[rawMaterailID].ChemicalPlaceholder2,step=1.0)
            ChemicalPlaceholder3 =st.number_input(label='Chemical Placeholder 3',min_value=1.0,value=result[rawMaterailID].ChemicalPlaceholder3,step=1.0)
            ChemicalPlaceholder4 =st.number_input(label='Chemical Placeholder 4',min_value=1.0,value=result[rawMaterailID].ChemicalPlaceholder4,step=1.0)
            Blainefineness = st.number_input(label='Blaine fineness',min_value=1.0,value=result[rawMaterailID].Blainefineness,step=1.0)
            SAI7 = st.number_input(label='Strength Activity Index (SAI) at 7 day',min_value=1.0,value=result[rawMaterailID].SAIat7,step=1.0)
            SAI28 = st.number_input(label='Strength Activity Index (SAI) at 28 day',min_value=1.0,value=result[rawMaterailID].SAIat28,step=1.0)
            Limereactivity = st.number_input(label='Lime reactivity',min_value=1.0,value=result[rawMaterailID].Limereactivity,step=1.0)
            Waterrequirement = st.number_input(label='Water requirement',min_value=1.0,value=result[rawMaterailID].Waterrequirement,step=1.0)
            Autoclaveexpansion = st.number_input(label='Autoclave expansion',min_value=1.0,value=result[rawMaterailID].Autoclaveexpansion,step=1.0)
            Aircontent = st.number_input(label='Air content',min_value=1.0,value=result[rawMaterailID].Aircontent,step=1.0)
            color = st.text_input('Color',value=result[rawMaterailID].color)
            PhysicalPlaceholder1 = st.number_input(label='Physical Placeholder 1', min_value=1.0, value=result[rawMaterailID].PhysicalPlaceholder1, step=1.0)
            PhysicalPlaceholder2 = st.number_input(label='Physical Placeholder 2', min_value=1.0, value=result[rawMaterailID].PhysicalPlaceholder2,step=1.0)
            PhysicalPlaceholder3 = st.number_input(label='Physical Placeholder 3', min_value=1.0, value=result[rawMaterailID].PhysicalPlaceholder3, step=1.0)
            PhysicalPlaceholder4 = st.number_input(label='Physical Placeholder 4', min_value=1.0, value=result[rawMaterailID].PhysicalPlaceholder4, step=1.0)
            st.write("Orignal PSD Table & Graph")
            uploaded_file_old_bytes = result[rawMaterailID].PSDTableandGraph
            st.image(uploaded_file_old_bytes)
            st.write("Do you want to modify PSD Table & Graph?")
            uploaded_file_new_bytes = st.file_uploader("PSD Table & Graph")
            if uploaded_file_new_bytes is not None:
                uploaded_file_old_bytes = uploaded_file_new_bytes

elif app_mode == "Material Sample":
    st.title("Material Sample")
    if add_radio == "Add":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT rawMatID,MaterialType FROM {RawMaterialTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        if rows:
            bMaterailIDList = {}
            for row in rows:
                bMaterailIDList[row[0]]=row[1]
            col1, col2 = st.columns(2)
            with col1:
                RawMaterailId = st.selectbox("Raw Material Id",bMaterailIDList)
            with col2:
                RawMaterailType = st.text_input('Raw Material Type',value=bMaterailIDList[RawMaterailId])     
                  
        DeliveryDate = st.date_input("Delivery Date")
        AvailableCH = st.number_input(label='Available CH',min_value=1.0,value=1.0,step=1.0)
        AvailableCaO = st.number_input(label='Available CaO',min_value=1.0,value=1.0,step=1.0)
        CO2uptake = st.number_input(label='CO2 uptake',min_value=1.0,value=1.0,step=1.0)
        Maximumtemperature = st.number_input(label='Maximum temperature',min_value=1.0,value=1.0,step=1.0)
        AreaUnderTheCurve = st.number_input(label='Area under the curve',min_value=1.0,value=1.0,step=1.0)
        uploaded_file_FTIR = st.file_uploader("Choose FTIR Image")
        if uploaded_file_FTIR is not None:
            bytes_data = uploaded_file_FTIR.read()
            st.image(uploaded_file_FTIR, caption=uploaded_file_FTIR.name)
        uploaded_file_XRD = st.file_uploader("Choose XRD Image")
        if uploaded_file_XRD is not None:
            bytes_data = uploaded_file_XRD.read()
            st.image(uploaded_file_XRD, caption=uploaded_file_XRD.name)
        uploaded_file_XRF = st.file_uploader("Choose XRF Image")
        if uploaded_file_XRF is not None:
            bytes_data = uploaded_file_XRF.read()
            st.image(uploaded_file_XRF, caption=uploaded_file_XRF.name)
        uploaded_Data_sheet = st.file_uploader("Choose Data Sheet",type="pdf")
        if uploaded_Data_sheet is not None:
            bytes_data = uploaded_Data_sheet.read()
            #st.image(uploaded_Data_sheet, caption=uploaded_file.name)
    elif add_radio == "Edit":
        conn = connect_to_db_aws()
        cur  = conn.cursor()
        select_all_rows_query = f'SELECT * FROM {MaterialSampleTableName}'
        cur.execute(select_all_rows_query)
        rows = cur.fetchall()
        MaterialSample = namedtuple(MaterialSampleTableName,[ 'rawMatID', 'DeliveryDate', 'AvailableCH', 'AvailableCaO', 'CO2uptake','Maximumtemperature','Areaunderthecurve','FTIRGraph','XRDGraph','XRFGraph','DataSheet'])
        if rows:
            result = {}
            MaterialSampleIDList = list()
            for row in rows:
                result[row[0]] = MaterialSample(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
                MaterialSampleIDList.append(row[0])
        
            MaterialSampleId = st.selectbox("Material Sample Id",MaterialSampleIDList)
            select_all_rows_query = f'SELECT rawMatID,MaterialType FROM {RawMaterialTableName}'
            cur.execute(select_all_rows_query)
            rows = cur.fetchall()
            if rows:
                bMaterailIDList = {}
                for row in rows:
                    bMaterailIDList[row[0]]=row[1]
                col1, col2 = st.columns(2)
                with col1:
                    RawMaterailId = st.selectbox("Raw Material Id",bMaterailIDList)
                with col2:
                    RawMaterailType = st.text_input('Raw Material Type',value=bMaterailIDList[RawMaterailId])  
                
            DeliveryDate = st.date_input("Delivery Date",value=result[MaterialSampleId].DeliveryDate)
            AvailableCH = st.number_input(label='Available CH',min_value=1.0,value=result[MaterialSampleId].AvailableCH,step=1.0)
            AvailableCaO = st.number_input(label='Available CaO',min_value=1.0,value=result[MaterialSampleId].AvailableCaO,step=1.0)
            CO2uptake = st.number_input(label='CO2 uptake',min_value=1.0,value=result[MaterialSampleId].CO2uptake,step=1.0)
            Maximumtemperature = st.number_input(label='Maximum temperature',min_value=1.0,value=result[MaterialSampleId].Maximumtemperature ,step=1.0)
            AreaUnderTheCurve = st.number_input(label='Area under the curve',min_value=1.0,value=result[MaterialSampleId].Areaunderthecurve ,step=1.0)

            uploaded_file_FTIR = st.file_uploader("Existing FTIR Image as below, Do you wan to change FTIR Image? then Choose new FTIR Image.")
            FTIRGraphImage = st.image(result[MaterialSampleId].FTIRGraph)
            if uploaded_file_FTIR is not None:
                st.write("New FTIR Image, As below")
                bytes_data = uploaded_file_FTIR.read()
                st.image(uploaded_file_FTIR)
            
            st.write("Existing XRD Image, Do you wan to change XRD Image?")
            XRDImage =st.image(result[MaterialSampleId].XRDGraph)
            uploaded_file_XRD = st.file_uploader("Choose XRD Image")
            if uploaded_file_XRD is not None:
                bytes_data = uploaded_file_XRD.read()
                st.image(uploaded_file_XRD)
            
            st.write("Existing XRF Image, Do you wan to change XRF Iamge?")
            st.image(result[MaterialSampleId].XRFGraph)      
            uploaded_file_XRF = st.file_uploader("Choose XRF Image")
            if uploaded_file_XRF is not None:
                bytes_data = uploaded_file_XRF.read()
                st.image(uploaded_file_XRF)
        
            uploaded_Data_sheet_byte = result[MaterialSampleId].DataSheet
            st.write("Do you wan to change Existing Data Sheet?") 
            uploaded_Data_sheet = st.file_uploader("Choose Data Sheet",type="pdf")
            if uploaded_Data_sheet is not None:
                uploaded_Data_sheet_byte = uploaded_Data_sheet.read()

elif app_mode == "Concrete Product":
    st.title("Concrete Product")
    if add_radio == "Add":
        ProductType = st.selectbox("Product Type",("CMU","Paver","SRW"))
        ProductDescription = st.text_input('Product Description')
        col1, col2 = st.columns(2)
        with col1:
            MixDesignName = st.selectbox("MixDesign ID",("1","2"))
        with col2:
            bProducerName1 = st.text_input('MixDesign Name')
        col1, col2 = st.columns(2)
        with col1:
            PlantID = st.selectbox("Plant ID",("1","2"))
        with col2:
            PlantName = st.text_input('Plant Name')
    elif add_radio == "Edit":
        col1, col2 = st.columns(2)
        with col1:
            CPID = st.selectbox("CPID",("CP1","CP2","CP3"))
        with col2:
            CPID = st.number_input(label='CPID',min_value=1.0,value=1.0,step=1.0)
        ProductType = st.selectbox("Product Type",("P1","P2","P3"))
        ProductDescription = st.text_input('Product Description')
        col1, col2 = st.columns(2)
        with col1:
            MixDesignName = st.selectbox("MixDesign ID",("1","2"))
        with col2:
            bProducerName1 = st.text_input('MixDesign Name')
        col1, col2 = st.columns(2)
        with col1:
            PlantID = st.selectbox("Plant ID",("1","2"))
        with col2:
            PlantName = st.text_input('Plant Name')
elif app_mode == "Trial":
    st.title("Trial")
    if add_radio == "Add":
        col1, col2 = st.columns(2)
        with col1:
            CPID = st.selectbox("CPID",("CP1","CP2","CP3"))
            MixDesignID = st.selectbox("MixDesign ID",("1","2"))
            PlantID = st.selectbox("Plant ID",("1","2"))
        with col2:
            CPName = st.text_input('CP Name')
            bProducerName1 = st.text_input('MixDesign Name')
            PlantName = st.text_input('Plant Name')
        TrialNotes = st.text_input('Trial Notes')
        TrialType = st.text_input('Trial Type')
        TrialDate = st.date_input("Trial Date")

    elif add_radio == "Edit":
        col1, col2 = st.columns(2)
        with col1:
            CPID = st.selectbox("CPID",("CP1","CP2","CP3"))
            MixDesignID = st.selectbox("MixDesign ID",("1","2"))
            PlantID = st.selectbox("Plant ID",("1","2"))
        with col2:
            CPName = st.text_input('CP Name')
            bProducerName1 = st.text_input('MixDesign Name')
            PlantName = st.text_input('Plant Name')
        TrialNotes = st.text_input('Trial Notes')
        TrialType = st.text_input('Trial Type')
        TrialDate = st.date_input("Trial Date")
elif app_mode == "TGA":
    st.title("TGA")
    if add_radio == "Add":
        CO2Uptake = st.number_input(label='CO2 Uptake',min_value=1.0,value=1.0,step=1.0)
        Wn = st.number_input(label='Wn',min_value=1.0,value=1.0,step=1.0)
        CH = st.number_input(label='CH',min_value=1.0,value=1.0,step=1.0)
        Ettrigite = st.number_input(label='Ettrigite',min_value=1.0,value=1.0,step=1.0)
        col1, col2 = st.columns(2)
        with col1:
            CPID = st.selectbox("TrialID",("CP1","CP2","CP3"))
            strengthTestID= st.selectbox("strengthTestID",("S1","S2","S33"))
        with col2:
            CPName = st.text_input('CP Name')
            strengthTesName= st.text_input('strengthTes Name')
    elif add_radio == "Edit":
        CO2Uptake = st.number_input(label='CO2 Uptake',min_value=1.0,value=1.0,step=1.0)
        Wn = st.number_input(label='Wn',min_value=1.0,value=1.0,step=1.0)
        CH = st.number_input(label='CH',min_value=1.0,value=1.0,step=1.0)
        Ettrigite = st.number_input(label='Ettrigite',min_value=1.0,value=1.0,step=1.0)
        col1, col2 = st.columns(2)
        with col1:
            CPID = st.selectbox("TrialID",("CP1","CP2","CP3"))
            strengthTestID= st.selectbox("strengthTestID",("S1","S2","S33"))
        with col2:
            CPName = st.text_input('CP Name')
            strengthTesName= st.text_input('strengthTes Name')
        
if st.button("Submit"):
    conn = connect_to_db_aws()
    cur  = conn.cursor()
    if app_mode == "Block Producer":
        if add_radio == "Add":
            query = f'INSERT INTO {BlockProducerTableName} (`bProducerName`, `NumberofBlockPlants`, `Notes`) VALUES (%s, %s, %s )'
            query_values= [bProducerName,bProducerNumber,bProducerNotes]
        elif add_radio == "Edit":
            query = f'UPDATE {BlockProducerTableName} SET `bProducerName`= %s,`NumberofBlockPlants`= %s,`Notes`= %s WHERE `bProducerId`= %s'
            query_values = [bProducerName,bProducerNumber,bProducerNotes,bProducerId]
    elif app_mode == "Block Plant": 
        if add_radio == "Add":
            query = f'INSERT INTO {BlockPlantTableName} (`bProducerID`, `bRegion`, `bAddress`, `CanUseRailroad`,                                         `ProductOffer_ProductionVolume`, `Power_CO2_source`, `Jan_Month_Avg_Temp`, `Feb_Month_Avg_Temp`, `Mar_Month_Avg_Temp`,                       `April_Month_Avg_Temp`, `May_Month__Avg_Temp`, `June_Month_Avg_Temp`, `July_Month_Avg_Temp`, `August_Month_Avg_Temp`,                       `Sep_Month_Avg_Temp`, `Oct_Month_Avg_Temp`, `Nov_Month_Avg_Temp`, `Dec_Month_Avg_Temp`) \
             VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s )'
            query_values= [bProducerID, bPlantRegion, bPlantAddress, bcanUseRailRoad, bProductOffering, bPowerCo2Src, bPlantTempJan,                     bPlantTempFeb, bPlantTempMarch, bPlantTempApril, bPlantTempMay, bPlantTempJune, bPlantTempJully, bPlantTempAugust,                           bPlantTempSep, bPlantTempOct, bPlantTempNov,bPlantTempDec]
        elif add_radio == "Edit":
            query = f'UPDATE {BlockPlantTableName} SET `bProducerID`= %s, `bRegion`= %s, `bAddress`= %s,`CanUseRailroad`= %s,\
            `ProductOffer_ProductionVolume`=%s,`Power_CO2_source`=%s,`Jan_Month_Avg_Temp`=%s,`Feb_Month_Avg_Temp`=%s,\
            `Mar_Month_Avg_Temp`=%s, `April_Month_Avg_Temp`=%s,`May_Month__Avg_Temp`=%s,`June_Month_Avg_Temp`=%s,\
            `July_Month_Avg_Temp`=%s,`August_Month_Avg_Temp`=%s,`Sep_Month_Avg_Temp`=%s,`Oct_Month_Avg_Temp`=%s,\
            `Nov_Month_Avg_Temp`=%s,`Dec_Month_Avg_Temp`=%s WHERE `bPlantID` = %s'
            query_values = [bProducerID, bPlantRegion, bPlantAddress, bcanUseRailRoad, bProductOffering, bPowerCo2Src, bPlantTempJan,                   bPlantTempFeb, bPlantTempMarch, bPlantTempApril, bPlantTempMay, bPlantTempJune, bPlantTempJully, bPlantTempAugust,                           bPlantTempSep, bPlantTempOct, bPlantTempNov,bPlantTempDec,bPlantID]
    elif app_mode == "Material Supplier":
        if add_radio == "Add":
            query = f'INSERT INTO {MaterialSupplierTableName} (`MaterialSupplierName`) VALUES (%s)'
            query_values= [MaterailSupplierName]
        elif add_radio == "Edit":
            query = f'UPDATE {MaterialSupplierTableName} SET `MaterialSupplierName`=  %s WHERE `mattSupplierID`= %s'
            query_values = [MaterailSupplierName,MaterailSupplierId]
    elif app_mode == "Raw Material":
        if add_radio == "Add":
            query = f'INSERT INTO {RawMaterialTableName} (`mattSupplierID`,`MaterialType`, `Address(Source)`,`Density`, `Sieve4`, `Sieve30`, `Sieve100`, `Sieve325`, `WaterAbsorption`, `Finenessmodulus`, `SiO2`, `Al2O3`, `Fe2O3`, `CaO`, `FreeLime`, `MgO`, `SO3`, `Na2O`, `K2O`, `CaCO3`, `Fluorine`, `Chloride`, `TotalAlkalis`, `AvailableAlkalis`, `LossonIgnition`, `Moisturecontent`, `Insolubleresidue`, `Freewater`, `ChemicalPlaceholder1`,`ChemicalPlaceholder2`,`ChemicalPlaceholder3`,`ChemicalPlaceholder4`,`Blainefineness`,`SAIat7`,`SAIat28`,`Limereactivity`,`Waterrequirement`,`Autoclaveexpansion`,`Aircontent`,`color`,`PhysicalPlaceholder1`,`PhysicalPlaceholder2`,`PhysicalPlaceholder3`,`PhysicalPlaceholder4`,`PSDTableandGraph`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            query_values= [MaterailSupplierId,MaterialType, Address,Density ,Sieve_4,Sieve_30 ,Sieve_100, Sieve_325 ,Water_Absorption, Finenessmodulus ,SiO2 ,Al2O3 ,Fe2O3 ,CaO,FreeLime, MgO , SO3, Na2O ,K2O, CaCO3 ,Fluorine,Chloride, TotalAlkalis , AvailableAlkalis , LossonIgnition , Moisturecontent , Insolubleresidue ,Freewater ,ChemicalPlaceholder1 , ChemicalPlaceholder2 ,ChemicalPlaceholder3 , ChemicalPlaceholder4 ,Blainefineness , SAI7 ,SAI28 ,Limereactivity, Waterrequirement , Autoclaveexpansion, Aircontent , color , PhysicalPlaceholder1, PhysicalPlaceholder2, PhysicalPlaceholder3, PhysicalPlaceholder4,uploaded_file.read()]
        elif add_radio == "Edit":
            query = f'UPDATE {RawMaterialTableName} SET `mattSupplierID`= %s, `MaterialType`= %s, `Address(Source)`= %s,`Density`= %s,\
            `Sieve4`=%s,`Sieve30`=%s,`Sieve100`=%s,`Sieve325`=%s,`WaterAbsorption`=%s,`Finenessmodulus`=%s,`SiO2`=%s,`Al2O3`=%s,\
            `Fe2O3`=%s,`CaO`=%s,`FreeLime`=%s,`MgO`=%s,`SO3`=%s,`Na2O`=%s , `K2O`=%s, `CaCO3`=%s, `Fluorine`=%s, `Chloride`=%s, `TotalAlkalis`=%s, `AvailableAlkalis`=%s, `LossonIgnition`=%s, `Moisturecontent`=%s, `Insolubleresidue`=%s, `Freewater`=%s, `ChemicalPlaceholder1`=%s,`ChemicalPlaceholder2`=%s,`ChemicalPlaceholder3`=%s,`ChemicalPlaceholder4`=%s,`Blainefineness`=%s,`SAIat7`=%s,`SAIat28`=%s,`Limereactivity`=%s,`Waterrequirement`=%s,`Autoclaveexpansion`=%s,`Aircontent`=%s,`color`=%s,`PhysicalPlaceholder1`=%s,`PhysicalPlaceholder2`=%s,`PhysicalPlaceholder3`=%s,`PhysicalPlaceholder4`=%s,`PSDTableandGraph`=%s WHERE `rawMatID` = %s'
            query_values = [MaterailSupplierId,MaterialType, Address,Density ,Sieve_4,Sieve_30 ,Sieve_100, Sieve_325 ,Water_Absorption, Finenessmodulus ,SiO2 ,Al2O3 ,Fe2O3 ,CaO,FreeLime, MgO , SO3, Na2O ,K2O, CaCO3 ,Fluorine,Chloride, TotalAlkalis , AvailableAlkalis , LossonIgnition , Moisturecontent , Insolubleresidue ,Freewater ,ChemicalPlaceholder1 , ChemicalPlaceholder2 ,ChemicalPlaceholder3 , ChemicalPlaceholder4 ,Blainefineness , SAI7 ,SAI28 ,Limereactivity, Waterrequirement , Autoclaveexpansion, Aircontent , color , PhysicalPlaceholder1, PhysicalPlaceholder2, PhysicalPlaceholder3, PhysicalPlaceholder4,uploaded_file_old_bytes.read(),rawMaterailID]
    elif app_mode == "Material Sample":
        if add_radio == "Add":
            query = f'INSERT INTO {MaterialSampleTableName} (`rawMatID`,`DeliveryDate`,`AvailableCH`,`AvailableCaO`,`CO2uptake`,`Maximumtemperature`,`Areaunderthecurve`, `FTIRGraph`,`XRDGraph` ,`XRFGraph`,`DataSheet` ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            query_values= [RawMaterailId,DeliveryDate, AvailableCH, AvailableCaO, CO2uptake,Maximumtemperature,AreaUnderTheCurve, uploaded_file_FTIR.read(), uploaded_file_XRD.read(),uploaded_file_XRF.read() ,uploaded_Data_sheet.read()]
        elif add_radio == "Edit":
            query = f'UPDATE {MaterialSampleTableName} SET `rawMatID`=%s, `DeliveryDate`= %s ,`AvailableCH`= %s, `AvailableCaO`= %s, `CO2uptake`= %s, `Maximumtemperature`= %s,`Areaunderthecurve`= %s, `FTIRGraph`= %s,`XRDGraph`= %s ,`XRFGraph`= %s,`DataSheet`= %s WHERE `MatSampleID`= %s'
            query_values = [RawMaterailId, DeliveryDate, AvailableCH, AvailableCaO, CO2uptake, Maximumtemperature, AreaUnderTheCurve,uploaded_file_FTIR.read(),uploaded_file_XRD.read(),uploaded_file_XRF.read(),uploaded_Data_sheet.read(),MaterialSampleId]            
    try:
        cur.execute(query, query_values)
        conn.commit()
        conn.close()
        st.balloons()
    except mysql.connector.Error as e:
        st.write(e)

