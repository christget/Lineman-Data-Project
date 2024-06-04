import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import json
import numpy as np
from datetime import datetime

# initialize page config
st.set_page_config(page_title='Horganice Advance Analytics', page_icon=':bar_chart:', layout='wide')
st.title(':bar_chart: Horganice Advance Analytics')
st.markdown("<style>div.block-container{padding-top:1rem;}<style>", unsafe_allow_html=True)

# import data
apartment_file_path = 'processed_data/Jatujak_Putamonton_apartment.csv'
room_file_path = 'processed_data/Jatujak_Putamonton_roomType.csv'
location_file_path = 'processed_data/Jatujak_Putamonton_location.csv'
apartment_df = pd.read_csv(apartment_file_path)
room_df = pd.read_csv(room_file_path)
location_df = pd.read_csv(location_file_path)

# apartment_df = pd.read_csv('/Users/mymac1/iCloud Drive (Archive)/Documents/apartment-data-crawler/data/processed_data/Jatujak_Putamonton_apartment.csv')
# room_df = pd.read_csv('/Users/mymac1/iCloud Drive (Archive)/Documents/apartment-data-crawler/data/processed_data/Jatujak_Putamonton_roomType.csv')
# location_df = pd.read_csv('/Users/mymac1/iCloud Drive (Archive)/Documents/apartment-data-crawler/data/processed_data/Jatujak_Putamonton_location.csv')

st.sidebar.header('Geo Selection')
province = st.sidebar.multiselect('จังหวัด', options=apartment_df['province'].unique().tolist())

if not province:
    df = apartment_df.copy()
else:
    df = apartment_df[apartment_df['province'].isin(province)]

district = st.sidebar.multiselect('อำเภอ/เขต', options=df['district'].unique().tolist())

if not district:
    df2 = df.copy()
else:
    df2 = df[df['district'].isin(district)]

sub_district = st.sidebar.multiselect('ตำบล/แขวง', options=df2['subDistrict'].unique().tolist())

if not sub_district:
    df3 = df2.copy()
else:
    df3 = df2[df2['subDistrict'].isin(sub_district)]

if not province and not district and not sub_district:
    filter_df = apartment_df
elif not province and not district:
    filter_df = apartment_df[apartment_df['subDistrict'].isin(sub_district)]
elif not province and not sub_district:
    filter_df = apartment_df[apartment_df['district'].isin(district)]
elif not district and not sub_district:
    filter_df = apartment_df[apartment_df['province'].isin(province)]
elif not province:
    filter_df = apartment_df[apartment_df['subDistrict'].isin(sub_district)]
elif not district:
    filter_df = apartment_df[apartment_df['subDistrict'].isin(sub_district)]
elif not sub_district:
    filter_df = apartment_df[apartment_df['district'].isin(district)]
elif province and district and sub_district:
    filter_df = apartment_df[apartment_df['subDistrict'].isin(sub_district)]

st.sidebar.header('Location Selection')
location_fliter = st.sidebar.multiselect('ย่าน', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())# if province or district or sub_district else ) 
place_fliter = st.sidebar.multiselect('สถานที่ใกล้เคียง', options=location_df[(location_df['location'].isin(location_fliter)) & (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique() if location_fliter else location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['place'].unique())

if not location_fliter and not place_fliter:
    filter_df = filter_df
elif not place_fliter:
    filter_df = filter_df[filter_df['apartment_url'].isin(location_df[location_df['location'].isin(location_fliter)]['apartment_url'].unique())]
elif not location_fliter:
    filter_df = filter_df[filter_df['apartment_url'].isin(location_df[location_df['place'].isin(place_fliter)]['apartment_url'].unique())]
elif location_fliter and place_fliter:
    filter_df = filter_df[filter_df['apartment_url'].isin(location_df[location_df['place'].isin(place_fliter)]['apartment_url'].unique())]

st.subheader('Metric Cards')
how_metric = st.expander('รายละเอียด Metric Cards 🔍')
with how_metric:
    how = '''
        Metric Cards ในแต่ละหมวดหมู่จะแสดง ค่าสถิติพื้นฐาน (ความถี่ ค่าเฉลี่ย ค่าต่ำสุด และสูงสุด) ของแต่ละหมวดหมู่ ประกอบด้วย
        - จำนวนห้องพัก
        - ค่าเช่ารายเดือน
        - ค่าเช่ารายวัน
        - ค่าเช่าต่อตารางเมตร
        - ค่าไฟฟ้า
        - ค่าน้ำ (ยูนิต)
        - ค่าน้ำ (เหมาจ่าย)
    '''
    st.markdown(how)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('จำนวนห้องพัก')

with col2:
    cnt_apartment = st.metric('จำนวนหอพักทั้งหมด', value='{:,.0f}'.format(filter_df['apartment_url'].count()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('พื้นที่ห้องพัก')
with col2:
    min_sqmt = st.metric('พื้นที่ห้องต่ำสุด (ตรม)', value='{:,.2f}'.format(filter_df['minRoomSize'].min()))
with col3:
    max_sqmt = st.metric('พื้นที่ห้องสูงสุด (ตรม)', value='{:,.2f}'.format(filter_df['maxRoomSize'].max()))
with col4:
    avg_sqmt = st.metric('พื้นที่ห้องเฉลี่ย (ตรม)', value='{:,.2f}'.format(filter_df['avgRoomSize'].mean()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('ค่าเช่ารายเดือน')
with col2:
    min_monthly_rental = st.metric('ค่าเช่ารายเดือนต่ำสุด (฿)', value='{:,.2f}'.format(filter_df['minMonthlyRent'].min()))
with col3:
    max_monthly_rental = st.metric('ค่าเช่ารายเดือนสูงสุด (฿)', value='{:,.2f}'.format(filter_df['maxMonthlyRent'].max()))
with col4:
    avg_monthly_rental = st.metric('ค่าเช่ารายเดือนเฉลี่ย (฿)', value='{:,.2f}'.format(filter_df['minMonthlyRent'].median()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('ค่าเช่ารายวัน')
with col2:
    min_daily_rental = st.metric('ค่าเช่ารายวันต่ำสุด (฿)', value='{:,.2f}'.format(filter_df['minDailyRent'].min()))
with col3:
    max_daily_rental = st.metric('ค่าเช่ารายวันสูงสุด (฿)', value='{:,.2f}'.format(filter_df['minDailyRent'].max()))
with col4:
    avg_daily_rental = st.metric('ค่าเช่ารายวันเฉลี่ย (฿)', value='{:,.2f}'.format(filter_df['minDailyRent'].median()))

col1, col2, col3, col4 = st.columns([1, 1, 1,1 ])
with col1:
    st.write('ค่าเช่าต่อตารางเมตร')
with col2:
    min_rental_sqmt = st.metric('ค่าเช่ารายตารางเมตรต่ำสุด (฿)', value='{:,.2f}'.format(filter_df['sqmt_avgMonthlyRent'].min()))
with col3:
    max_rental_sqmt = st.metric('ค่าเช่ารายตารางเมตรสูงสุด (฿)', value='{:,.2f}'.format(filter_df['sqmt_avgMonthlyRent'].max()))
with col4:
    avg_rental_sqmt = st.metric('ค่าเช่ารายตารางเมตรเฉลี่ย (฿)', value='{:,.2f}'.format(filter_df['sqmt_avgMonthlyRent'].median()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('ค่าไฟฟ้า')
with col2:
    min_elec_unit = st.metric('ค่าไฟต่ำสุด (฿/ยูนิต)', value='{:.2f}'.format(filter_df['electricity'].min()))
with col3:
    max_elec_unit = st.metric('ค่าไฟสูงสุด (฿/ยูนิต)', value='{:.2f}'.format(filter_df['electricity'].max()))
with col4:
    avg_elec_unit = st.metric('ค่าไฟเฉลี่ย (฿/ยูนิต)', value='{:.2f}'.format(filter_df['electricity'].mean()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('ค่าน้ำ (ยูนิต)')
with col2:
    min_waterUnit_unit = st.metric('ค่าน้ำต่ำสุด (฿/ยูนิต)', value='{:.2f}'.format(filter_df['waterUnit'].min()))
with col3:
    max_waterUnit_unit = st.metric('ค่าน้ำสูงสุด (฿/ยูนิต)', value='{:.2f}'.format(filter_df['waterUnit'].max()))
with col4:
    avg_waterUnit_unit = st.metric('ค่าน้ำเฉลี่ย (฿/ยูนิต)', value='{:.2f}'.format(filter_df['waterUnit'].mean()))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.write('ค่าน้ำ (เหมาจ่าย)')
with col2:
    min_waterFix_unit = st.metric('ค่าน้ำต่ำสุด (฿/เดือน)', value='{:.2f}'.format(filter_df['waterFix'].min()))
with col3:
    max_waterFix_unit = st.metric('ค่าน้ำสูงสุด (฿/เดือน)', value='{:.2f}'.format(filter_df['waterFix'].max()))
with col4:
    avg_waterFix_unit = st.metric('ค่าน้ำเฉลี่ย (฿/เดือน)', value='{:.2f}'.format(filter_df['waterFix'].mean()))

st.subheader('ข้อมูลเชิงพื้นที่')
how_densMap = st.expander('รายละเอียด Density Map 🔍')
with how_densMap:
    how = '''
    แผนภูมิแผนที่แสดง ค่าสถิติเชิงพื้นที่ ได้แก่
    1. :blue[จำนวนตึก]: จำนวนตึกทั้งหมดในแต่ละพื้นที่
    2. :blue[ค่าเช่าห้อง]: ค่าเช่าห้องรายเดือนเฉลี่ยในแต่ละพื้นที่ (บาท)
    3. :blue[ค่าเช้าห้องตารางเมตร]: ค่าเช่าห้องรายเดือนเฉลี่ยต่อตารางเมตรในแต่ละพื้นที่(บาท/ตรม.)

    ซึ่งความเข้มข้นของสีบ่งบอกถึงมีจำนวน หรือมีค่าที่สูง
    '''
    st.markdown(how)
sub_district_geojson_file = 'subdistricts.geojson'
# sub_district_geojson_file = '/Users/mymac1/iCloud Drive (Archive)/Documents/apartment-data-crawler/subdistricts.geojson'

with open(sub_district_geojson_file) as f:
    sub_district_geojson_data = json.load(f)
for feature in sub_district_geojson_data['features']:
    feature['properties']['address'] = feature['properties']['tam_th'] + ', ' + feature['properties']['amp_th'] + ', ' + feature['properties']['pro_th']

# list only Chaing Mai apartment
sub_provinces = [feature['properties']['address'] for feature in sub_district_geojson_data['features'] if feature['properties']['pro_th'] in (filter_df['province'].unique())]
# sub_provinces = [feature['properties']['address'] for feature in sub_district_geojson_data['features'] if feature['properties']['pro_th'] == 'เชียงใหม่']
sub_district_df = pd.DataFrame(sub_provinces, columns=['address'])

# chart setting
col1, col2, col3 = st.columns([1,1,1])
with col1:
    select_fact = st.selectbox('Fact Value', options=['จำนวนตึก', 'จำนวนตึก (ร้อยละ)', 'ค่าเช่าห้อง', 'ค่าเช่าห้องตารางเมตร'])

if select_fact == 'จำนวนตึก':
    cal_df = filter_df.groupby(['province', 'district', 'subDistrict'])['apartment_url'].count().reset_index().rename(columns={'apartment_url' : select_fact})

if select_fact == 'จำนวนตึก (ร้อยละ)':
    cal_df = filter_df.groupby(['province', 'district', 'subDistrict'])['apartment_url'].count().reset_index().rename(columns={'apartment_url' : select_fact})
    total_count = cal_df[select_fact].sum()
    cal_df[select_fact] = round((cal_df[select_fact] / total_count) * 100, 2)

elif select_fact == 'ค่าเช่าห้อง':
    cal_df  = filter_df.groupby(['province', 'district', 'subDistrict'])['minMonthlyRent'].median().reset_index().rename(columns={'minMonthlyRent' : select_fact})

elif select_fact == 'ค่าเช่าห้องตารางเมตร':
    cal_df = filter_df.groupby(['province', 'district', 'subDistrict'])['sqmt_avgMonthlyRent'].median().reset_index().rename(columns={'sqmt_avgMonthlyRent' : select_fact})

cal_df['address'] = cal_df['subDistrict'] + ', ' + cal_df['district'] + ', ' + cal_df['province']
merged_df = sub_district_df.merge(cal_df, on='address', how='left')
merged_df['subDistrict'] = merged_df.apply(lambda row: row['subDistrict'] if pd.notna(row['subDistrict']) else row['address'].split(',')[0].strip(), axis=1)

merged_df[select_fact] = merged_df[select_fact].fillna(0)

colorscale = [[0, 'rgba(0,0,0,0)'], [0.0000000001, 'rgb(236,239,244)'], [1, 'rgb(8,48,107)']]

fig = px.choropleth_mapbox(merged_df, 
                    geojson=sub_district_geojson_data, 
                    locations='address', 
                    featureidkey='properties.address', 
                    color=select_fact,
                    hover_name='subDistrict',
                    color_continuous_scale=colorscale,
                    #color_continuous_midpoint=medium_value,
                    #projection='mercator',
                    center= {"lat": 13.7563, "lon": 100.5018} if not province else {"lat": filter_df[filter_df['province'].isin(province)]['lat'].median(), "lon": filter_df[filter_df['province'].isin(province)]['lon'].median()}, #18.766843	98.964878
                    mapbox_style='carto-darkmatter',#"carto-positron", 
                    zoom=7,
                    height=600
                )

fig.update_layout(coloraxis_colorbar=dict(
                x=0.05,
                y=-0.15,
                xanchor='left',
                yanchor='bottom',
                orientation='h'
))

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.subheader('การกระจายของข้อมูล')
how_dis = st.expander('รายละเอียดของ Distribution Chart 🔍')
with how_dis:
    how = '''
    กราฟ :blue[Histogram] ด้านล่างแสดงถึงการกระจายตัวของข้อมูล :red[ช่วยบอกว่าข้อมูลส่วนใหญ่กระจุกตัวอยู่ช่วงไหน และมีค่าต่ำสุด และสูงสุดที่เท่าไหร]
    - แกน :blue[x] คือ ช่วงของข้อมูล
    - แกน :blue[y] ตือ จำนวนข้อมูลที่ตกอยู่ในแต่ละช่วง
    '''
    st.markdown(how)
monthlyRental_hist = filter_df['minMonthlyRent']
fig = px.histogram(monthlyRental_hist, range_x=[0, 30000], nbins=30, height=300, title='ช่วงราคาค่าเช่ารายเดือน')
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=1.13,
    xanchor="right",
    x=0.9,
))
fig.update_layout(legend_title_text='')
fig.update_traces(name='ค่าเช่ารายเดือน')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

dailyRental_hist = filter_df['minDailyRent']
fig = px.histogram(dailyRental_hist, range_x=[0, 3000], height=300, title='ช่วงราคาค่าเช่ารายวัน')
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=1.13,
    xanchor="right",
    x=0.9,
))
fig.update_layout(legend_title_text='')
fig.update_traces(name='ค่าเช่ารายวัน')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

sqmt_MonthlyRental_hist = filter_df['sqmt_avgMonthlyRent']
fig = px.histogram(sqmt_MonthlyRental_hist, range_x=[0, 3000], height=300, title='ช่วงค่าเช่ารายเดือนต่อตารางเมตร')
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=1.13,
    xanchor="right",
    x=0.9,
))
fig.update_layout(legend_title_text='')
fig.update_traces(name='ค่าเช่าต่อตารางเมตร')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

sqmt_hist = filter_df['avgRoomSize']
fig = px.histogram(sqmt_hist, range_x=[0, 300], height=300, title='พื้นที่ห้องตารางเมตร')
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="top",
    y=1.13,
    xanchor="right",
    x=0.9,
))
fig.update_layout(legend_title_text='')
fig.update_traces(name='พื้นที่ห้อง (ตรม)')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.subheader('สิ่งอำนวยความสะดวก')
how_popAmen = st.expander('รายละเอียดของ Popular Amenity Chart 🔍')
with how_popAmen:
    how = '''
    **Popular Amenity Chart**: กราฟแสดงความนิยมของสิ่งอำนวยความสะดวกของหอพักทั้งหมด
    โดยจะแสดงจำนวนหอพักในแต่ละสิ่งอำนวยความสะดวก เรียงลำดับจากมากไปน้อย
    - แกน :blue[x] คือ ประเภทของสิ่งอำนวยความสะดวกทั้งหมด
    - แกน :blue[y] คือ จำนวนหอพักที่มีสิ่งอำนวยความสะดวกดังกล่าว
    '''
    st.markdown(how)
amenities = ['ac', 'furniture', 'waterHeater', 'fan', 'carParking', 'wifi', 'cable', 'cctv', 'tv', 'fridge', 'sofa', 'desk', 'stove',
             'telephone', 'pet', 'smoking', 'motorbikeParking', 'elevator', 'pool', 'gym', 'keyCard', 
             'fingerPrint', 'security', 'restaurant', 'miniMart', 'laundry', 'salon', 'evCharging']

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    rent_interval = st.multiselect('Rental Price', options=filter_df['rent_interval'].sort_values().unique())

if rent_interval:
    cnt_amenity = filter_df[filter_df['rent_interval'].isin(rent_interval)][amenities].astype('int64').sum().reset_index().rename(columns={'index' : 'amenity', 0: 'count_amenity'})
    mean_rents = {amenity: filter_df[(filter_df['rent_interval'].isin(rent_interval)) & (filter_df[amenity])]['minMonthlyRent'].mean() for amenity in amenities}

else:
    cnt_amenity = filter_df[amenities].astype('int64').sum().reset_index().rename(columns={'index' : 'amenity', 0: 'count_amenity'})
    mean_rents = {amenity: filter_df[filter_df[amenity]]['minMonthlyRent'].mean() for amenity in amenities}
    
cnt_amenity = cnt_amenity.sort_values(by='count_amenity', ascending=False)
avg_amenity = pd.DataFrame(mean_rents, index=['avg_monthlyRent']).transpose().reset_index().rename(columns={'index' : 'amenity'}).sort_values(by='avg_monthlyRent', ascending=False)

fig = px.bar(cnt_amenity, 
                x='amenity', 
                y='count_amenity', 
                text= ['{:.0f}'.format(x) for x in cnt_amenity['count_amenity']], 
                title= "สิ่งอำนวยความสะดวก ยอดนิยม",
                color='count_amenity'
            )
fig.update_yaxes(title_text = "จำนวนตึก")
fig.update_xaxes(tickmode='linear', tick0=0, dtick=0.1)
fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

how_avgRent = st.expander('รายละเอียดของ Rental by Amenity 🔍')
with how_avgRent:
    how = '''
    **Rental Amenity Chart**: กราฟแสดงค่าเช่ารายเดือนเฉลี่ยในแต่ละสิ่งอำนวยความสะดวก เรียงลำดับจากมากไปน้อย
    - แกน :blue[x] คือ ประเภทของสิ่งอำนวยความสะดวกทั้งหมด
    - แกน :blue[y] คือ ค่าเช่ารายเดือนเฉลี่ย
    '''
    st.markdown(how)
fig = px.bar(avg_amenity,
             x='amenity',
             y='avg_monthlyRent',
             text = ['{:,.2f}'.format(x) for x in avg_amenity['avg_monthlyRent']],
             title= 'ค่าเช่าเฉลี่ย ในแต่ละสิ่งอำนวยความสะดวก',
             color= 'avg_monthlyRent')

fig.update_yaxes(title_text = "จำนวนตึก")
fig.update_xaxes(tickmode='linear', tick0=0, dtick=0.1)
fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.write('**Total Amenities by Rental Price Interval**')
how_totalAmen = st.expander('รายละเอียดตาราง Total Amenity by Rental Price Interval 🔍')
with how_totalAmen:
    how = '''
    **ตาราง Total Amenity by Rental Price Interval:** ตารางแสดงความหนาแน่นของจำนวนหอพักทั้งหมดแบ่งตามสิ่งอำนวยความสะดวก และช่วงราคาเช่ารายเดือน
    
    :red[วัตถุประสงค์] คือ สังเกตว่าในแต่ละช่วงราคานั้นสิ่งอำนวยความสะดวกไหนที่หอพักส่วนใหญ่ในราคานั้นๆ มี
    - :blue[column] คือ ประเภทสิ่งอำนวยความสะดวก
    - :blue[index] คือ ช่วงค่าเช่ารายเดือน
    - :blue[value] คือ จำนวนหอพักทั้งหมด
    '''
    st.markdown(how)

labels = ['0-1k', '1k-2k', '2k-3k', '3k-4k', '4k-5k', '5k-6k', '6k-7k', '7k-8k', '8k-9k', '9k-10k', '10k+']

col1, col2, col3 = st.columns([1, 1, 0.4])
with col1:
    price_interval = st.multiselect('ช่วงค่าเช่า', options=labels)
with col2:
    st.markdown("""
        <style>
        div.stCheckbox {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    amen_normalize = st.toggle('ร้อยละ')

if price_interval:
    amenity_pivot = filter_df[filter_df['rent_interval'].isin(price_interval)].pivot_table(index='rent_interval', values=amenities, aggfunc='sum', fill_value=0).reindex(price_interval).fillna(0).astype(int)
    export_amenity_pivot = filter_df[filter_df['rent_interval'].isin(price_interval)][['apartment_url', 'address', 'rent_interval'] + amenities]
else:
    amenity_pivot = filter_df.pivot_table(index='rent_interval', values=amenities, aggfunc='sum', fill_value=0).reindex(labels).fillna(0).astype(int)
    export_amenity_pivot = filter_df[['apartment_url', 'address', 'rent_interval'] + amenities]

if amen_normalize:
    amenity_pivot = amenity_pivot.div(amenity_pivot.sum(axis=1), axis=0).multiply(100).astype(float)

with col3:
    st.markdown("""
        <style>
        div.stDownloadButton > button {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.download_button(
        label='Export to CSV',
        data=export_amenity_pivot.to_csv().encode('utf-8'),
        file_name=f'rent_amenity_pivot_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

if price_interval and not amen_normalize:
    st.write(amenity_pivot.style.background_gradient(cmap='Blues', vmin=0, vmax=0 if amenity_pivot.values.max() == 0 else amenity_pivot.values.max()))
elif price_interval and amen_normalize:
    st.write(amenity_pivot.style.format('{:.2f}').background_gradient(cmap='Blues', vmin=0, vmax=0 if amenity_pivot.values.max() == 0 else amenity_pivot.values.max()))
elif amen_normalize:
    st.write(amenity_pivot.style.format('{:.2f}').background_gradient(cmap='Blues', axis=1))
elif not price_interval and not amen_normalize:
    st.write(amenity_pivot.style.background_gradient(cmap='Blues', axis=1))

st.write('**Total Amenity Available by Rent Price Interval**')
how_totalAvailAmen = st.expander('รายละเอียดตาราง Total Amenitiy Available by Rent Price Interval 🔍')
with how_totalAvailAmen:
    how = '''
    **ตาราง Total Amenity Available by Rent Price Interval:** ตารางแสดงจำนวนห้องพัก ณ ช่วงราคาต่างๆ ของสิ่งอำนวยความสะดวกที่ถูกเลือก
    
    :red[วัตถุประสงค์] คือ สังเกตว่าหอพักที่มีสิ่งอำนวยความสะดวกที่เลือกนั้นส่วนใหญ่มีราคาค่าเช่ารายเดือนอยู่ที่ช่วงเท่าไหร่
    - :blue[column] คือ ช่วงราคาค่าเช่ารายเดือน
    - :blue[index] คือ สิ่งอำนวยความสะดวกที่ถูกเลือก
    - :blue[value] คือ จำนวนหอพักที่มีสิ่งอำนวยความสะดวกที่ถูกเลือกดังกล่าว
    '''
    st.markdown(how)
col1, col2, col3 = st.columns([1,1,0.4])
with col1:
    amen = st.selectbox('Amenity', options=amenities)
with col2:
    st.markdown("""
        <style>
        div.stCheckbox {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    isAmen_normalize = st.toggle('ร้อยละ ')
if isAmen_normalize:
    isAmen_pivot = filter_df[filter_df[amen] == True][[amen, 'rent_interval']].pivot_table(index=amen, columns='rent_interval', aggfunc='size', fill_value=0).reindex(columns=labels).fillna(0).astype(int)
    isAmen_pivot = isAmen_pivot.div(isAmen_pivot.sum(axis=1), axis=0).multiply(100).astype(float)
    st.write(isAmen_pivot.style.format('{:.2f}').background_gradient(cmap='Blues', vmin=0, vmax=0 if isAmen_pivot.values.max().size == 0 else isAmen_pivot.values.max()))
else:
    isAmen_pivot = filter_df[filter_df[amen] == True][[amen, 'rent_interval']].pivot_table(index=amen, columns='rent_interval', aggfunc='size', fill_value=0).reindex(columns=labels).fillna(0).astype(int)

if not isAmen_normalize:
    st.write(isAmen_pivot.style.format('{:.0f}').background_gradient(cmap='Blues', vmin=0, vmax=0 if isAmen_pivot.values.max().size == 0 else isAmen_pivot.values.max()))

export_isAmen_pivot = filter_df[filter_df[amen] == True][['apartment_url', 'address', 'rent_interval'] + amenities]

with col3:
    st.markdown("""
        <style>
        div.stDownloadButton > button {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.download_button(
        label='Export to CSV',
        data=export_isAmen_pivot.to_csv().encode('utf-8'),
        file_name=f'isAmenity_pivot_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

st.subheader('สิ่งอำนวยความสะดวก x สถานที่')
col1, col2, col3, col4 = st.columns([1, 1, 1, 0.6])
with col1:
    locationType = st.selectbox('ย่าน', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())
with col2:
    place = st.multiselect('สถานที่', options=location_df[(location_df['location'] == locationType) & (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique())
with col3:
    value = st.selectbox('Value', options=['จำนวนหอพัก', 'จำนวนหอพัก (ร้อยละ)', 'ค่าเช่าเฉลี่ย', 'ค่าเช่าเฉลี่ยต่อตารางเมตร'])

amen_location_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                          (location_df['location'] == locationType)]

if place:
    amen_location_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) & 
                          (location_df['location'] == locationType) &
                          (location_df['place'].isin(place))]

#location_df
amen_df = amen_location_df.merge(filter_df[['apartment_url','ac', 'furniture', 'waterHeater', 'fan', 'carParking', 'wifi', 'cable', 'cctv', 'tv', 'fridge', 'sofa', 'desk', 'stove',
             'telephone', 'pet', 'smoking', 'motorbikeParking', 'elevator', 'pool', 'gym', 'keyCard', 
             'fingerPrint', 'security', 'restaurant', 'miniMart', 'laundry', 'salon', 'evCharging']],
             on='apartment_url',
             how='left')

melted_data = pd.melt(amen_df, id_vars=['apartment_url', 'place', 'avgMonthlyRent', 'sqmt_avgMonthlyRent'], value_vars=amenities, var_name='amenity', value_name='value')

# Filter out rows where the value is False
melted_data = melted_data[melted_data['value'] == True]

if value == 'จำนวนหอพัก':
    locationAmen_pivot = melted_data.pivot_table(index='place', columns='amenity', values='apartment_url', aggfunc='count', fill_value=0).round(2)
if value == 'จำนวนหอพัก (ร้อยละ)':
    locationAmen_pivot = melted_data.pivot_table(index='place', columns='amenity', values='apartment_url', aggfunc='count', fill_value=0).round(2)
    place_totals = locationAmen_pivot.sum(axis=1)
    locationAmen_pivot = (locationAmen_pivot.div(place_totals, axis=0) * 100).round(2)
    styled_df = locationAmen_pivot.style.format("{:.2f}").background_gradient(cmap='Blues', axis=None)
if value == 'ค่าเช่าเฉลี่ย':
    locationAmen_pivot = melted_data.pivot_table(index='place', columns='amenity', values='avgMonthlyRent', aggfunc='median', fill_value=0).round(2)
if value == 'ค่าเช่าเฉลี่ยต่อตารางเมตร':
    locationAmen_pivot = melted_data.pivot_table(index='place', columns='amenity', values='sqmt_avgMonthlyRent', aggfunc='median', fill_value=0).round(2)

if value != 'จำนวนหอพัก (ร้อยละ)':
    styled_df = locationAmen_pivot.style.format("{:,.0f}").background_gradient(cmap='Blues', axis=1)

export_xLocation = amen_df[['apartment_url', 'place', 'avgMonthlyRent', 'sqmt_avgMonthlyRent'] + amenities]

with col4:
    st.markdown("""
        <style>
        div.stDownloadButton > button {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.download_button(
        label='Export to CSV',
        data=export_xLocation.to_csv().encode('utf-8'),
        file_name=f'amenity&location_{datetime.now().strftime("%Y-%m-%d")}.csv',
        mime='text/csv'
    )

st.write('**Total Amenity by Place**')
how_amenLocation = st.expander('รายละเอียดตาราง Total Amenity by Place 🔍')
with how_amenLocation:
    how = '''
    **ตาราง Total Amenity by Place:** ตารางแสดงความหนาแน่นของจำนวนหอพักแบ่งตามสิ่งอำนวยความสะดวก ในสถานที่ต่างๆ
    
    :red[วัตถุประสงค์] คือ สังเกตว่าหอพักที่อยู่ใกล้สถานที่ต่างๆ นั้นส่วนใหญ่มีสิ่งอำนวยความสะดวกอะไรบ้าง
    - :blue[column] คือ ประเภทสิ่งอำนวยความสะดวก
    - :blue[index] คือ สถานที่
    - :blue[value] ประกอบไปด้วยค่า
        - จำนวนหอพัก
        - ค่าเช่าเฉลี่ยรายเดือน
        - ค่าเช่าเฉลี่ยต่อตารางเมตร

    :red[**Note**]: หากมีการเลือกสถานที่ ใน `สถานที่ selectbox` จะมี chart เพิ่มขึ้นมา 2 charts ได้แก่
    - **Popular Amenity:** กราฟแสดงสิ่งอำนวยความสะดวกยอดนิยมในระแวก
    - **Average Monthly Rent by Amenity:** กราฟแสดงค่าเช่าเฉลี่ยในแต่ละสิ่งอำนวยความสะดวกในระแวก
    '''
    st.markdown(how)
st.write(styled_df, unsafe_allow_html=True)

if place:
    col1, col2 = st.columns([1, 1])
    with col1:
        filter_df = filter_df[filter_df['apartment_url'].isin(location_df[
                (location_df['location'] == locationType) &
                (location_df['place'].isin(place))
            ]['apartment_url'].unique())]
    
        cnt_amenity = filter_df[amenities].astype('int64').sum().reset_index().rename(columns={'index' : 'amenity', 0: 'count_amenity'})
        cnt_amenity = cnt_amenity.sort_values(by='count_amenity', ascending=False)

        fig = px.bar(cnt_amenity, 
                        x='amenity', 
                        y='count_amenity', 
                        text= ['{:.0f}'.format(x) for x in cnt_amenity['count_amenity']], 
                        title= f"สิ่งอำนวยความสะดวกยอดนิยม ระแวก {place[0]}",
                        color='count_amenity'
                    )
        fig.update_yaxes(title_text = "Amenity")
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=0.1)
        # fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        locationAmen_pivot = melted_data.pivot_table(index='place', columns='amenity', values='avgMonthlyRent', aggfunc='median', fill_value=0).round(2)
        avg_locationAmen = pd.DataFrame({
            'amenity' : locationAmen_pivot.columns,
            'avgMonthlyRent' : locationAmen_pivot.loc[locationAmen_pivot.index[0]]
        })
        avg_locationAmen = avg_locationAmen.sort_values(by='avgMonthlyRent', ascending=False)
        fig = px.bar(avg_locationAmen, 
                     x='amenity', 
                     y='avgMonthlyRent', 
                     title=f'ค่าเช่าเฉลี่ย ระแวก {place[0]}',
                     color='avgMonthlyRent')
        fig.update_yaxes(title_text = "Average Rental")
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=0.1)
        st.plotly_chart(fig, use_container_width=True)

st.subheader('สถานที่')

st.write('**Total Apartment by Distance and Rental Price Interval**')
how_location = st.expander('รายละเอียดตาราง Total Apartment by Distance and Rental Price Interval 🔍')
with how_location:
    how = '''
    **ตาราง Total Apartment by Distance and Rental Price Interval:** แสดงความหนาแน่นของจำนวนหอพักที่อยู่ในช่วงราคาค่าเช่า และระยะห่างจากทำเลต่างๆ
    
    :red[วัตถุประสงค์] คือ สังเกตว่าระยะทางระหว่างย่าน หรือสถานที่กับหอพัก มีผลต่อราคาค่าเช่ารายเดือนหรือไม่
    - :blue[column] คือ ช่วงราคาค่าเช่า
    - :blue[index] คือ ช่วงระยะห่างระหว่างหอพัก และทำเล
    - :blue[value] คือ จำนวนหอพัก
    '''
    st.markdown(how)
dis_labels = ['0m-300m', '300m-600m', '600m-900m', '900m-1.2km', '1.2km-1.5km', '1.5km-1.8km', '1.8km-2.1km', '2.1km-2.4km', '2.4km-2.7km', '2.7km-3.0km', '3.0km+']
col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    # st.markdown(
    # """
    # <style>
    #     .stSelectbox > div[data-baseweb="select"] {
    #         margin-top: -50px; 
    #     }
    # </style>
    # """,
#     unsafe_allow_html=True
# )
    locationType = st.selectbox('ย่าน ', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())
with col2:
    place = st.multiselect('สถานที่ ', options=location_df[(location_df['location'] == locationType) &  (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique())
with col3:
    st.markdown("""
        <style>
        div.stCheckbox {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    location_normalize = st.toggle('ร้อยละ  ')

if place:
    place_df = filter_df[filter_df['apartment_url'].isin(location_df[
        (location_df['location'] == locationType) &
        (location_df['place'].isin(place))
    ]['apartment_url'].unique())]
else:
    place_df = filter_df

if locationType == 'สถานศึกษา':
    distance_pivot = place_df[['interval_สถานศึกษา', 'rent_interval']].pivot_table(index='interval_สถานศึกษา', columns='rent_interval', aggfunc='size', fill_value=0).reindex(index=dis_labels, columns=labels).fillna(0).astype(int)
elif locationType == 'ถนน/ซอยใกล้เคียง':
    distance_pivot = place_df[['interval_ถนน/ซอยใกล้เคียง', 'rent_interval']].pivot_table(index='interval_ถนน/ซอยใกล้เคียง', columns='rent_interval', aggfunc='size', fill_value=0).fillna(0).astype(int)
elif locationType == 'ห้างสรรพสินค้า/ตลาด':
    distance_pivot = place_df[['interval_ห้างสรรพสินค้า/ตลาด', 'rent_interval']].pivot_table(index='interval_ห้างสรรพสินค้า/ตลาด', columns='rent_interval', aggfunc='size', fill_value=0).reindex(index=dis_labels, columns=labels).fillna(0).astype(int)
elif locationType == 'ย่านต่างๆใกล้เคียง':
    distance_pivot = place_df[['interval_ย่านต่างๆใกล้เคียง', 'rent_interval']].pivot_table(index='interval_ย่านต่างๆใกล้เคียง', columns='rent_interval', aggfunc='size', fill_value=0).reindex(index=dis_labels, columns=labels).fillna(0).astype(int)
elif locationType == 'ที่พักใกล้รถไฟฟ้า':
    distance_pivot = place_df[['interval_ที่พักใกล้รถไฟฟ้า', 'rent_interval']].pivot_table(index='interval_ที่พักใกล้รถไฟฟ้า', columns='rent_interval', aggfunc='size', fill_value=0).reindex(index=dis_labels, columns=labels).fillna(0).astype(int)

distance_pivot = distance_pivot.rename_axis(f'{locationType}', axis='index')

if location_normalize:
    row_totals = distance_pivot.sum(axis=1)
    distance_pivot = (distance_pivot.div(row_totals, axis=0) * 100).round(2)
    distance_pivot = distance_pivot.apply(pd.to_numeric).style.format('{:.2f}').background_gradient(cmap='Blues', axis=1)

export_place = place_df[['apartment_url', 'address', 'rent_interval', 'interval_สถานศึกษา', 'interval_ถนน/ซอยใกล้เคียง', 'interval_ห้างสรรพสินค้า/ตลาด', 'interval_ย่านต่างๆใกล้เคียง']]

with col4:
    st.markdown("""
        <style>
        div.stDownloadButton > button {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.download_button(
        label='Export to CSV',
        data= export_place.to_csv().encode('utf-8'),
        file_name= f'place_rent&distance_interval_{datetime.now().strftime("%Y-%m-%d")}.csv',
        mime='text/csv'
    )
if not location_normalize:
    distance_pivot = distance_pivot.apply(pd.to_numeric).style.background_gradient(cmap='Blues', axis=1)
st.write(distance_pivot, unsafe_allow_html=True)

st.subheader('Optional')
optional_section = st.expander('Optional Section 🔍')
with optional_section:
    how_optional = '''
    **Note:** ส่วนนี้ประกอบไปด้วยกราฟที่มีความซับซ้อน วางไว้เป็น idea ในการพัฒนาต่อให้อ่านง่ายขึ้น 🧐
    '''
    st.markdown(how_optional)
    st.subheader('Place')

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        location = st.multiselect('ย่าน  ', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())
    with col2:
        place = st.multiselect('สถานที่  ', options=location_df[(location_df['location'].isin(location)) & (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique() if location else location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['place'].unique())
    with col3:
        st.markdown("""
        <style>
        div.stCheckbox {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
        if place:
            show_name = st.toggle("Show Place's Name",value=True)
        else:
            show_name = st.toggle("Show Place's Name")

    if not place and not location:
        place_agg_df = location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())] 
    elif not place:
        place_agg_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['location'].isin(location))]
    elif not location:
        place_agg_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['place'].isin(place))]
    elif location and place:
        place_agg_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                #    (location_df['location'].isin(location)) &
                                (location_df['place'].isin(place))]  

    plcae_agg_pivot = place_agg_df.groupby('place').agg(
                location=('location', 'first'),
                cnt_apartment=('apartment_url', 'count'),
                avg_distance=('distance', 'mean'),
                avg_monthlyRent=('avgMonthlyRent', 'mean'),
                avg_sqmtMonthlyRent=('sqmt_avgMonthlyRent', 'mean')
            ).reset_index()

    if show_name :
        fig = px.scatter(
            plcae_agg_pivot.query('avg_distance < 100000'),
            x='avg_distance',
            y='avg_monthlyRent',
            size='cnt_apartment',
            color='location',
            hover_name='place',
            text='place',
            size_max=60,
            labels={
                'avg_distance': 'Average Distance (m)',
                'avg_monthlyRent': 'Average Monthly Rent (THB)'
            },
            title='Scatter Bubble Plot of Avg Distance vs Avg Monthly Rent'
        )
        fig.update_traces(textposition='top center')
    else:
        fig = px.scatter(
            plcae_agg_pivot.query('avg_distance < 100000'),
            x='avg_distance',
            y='avg_monthlyRent',
            size='cnt_apartment',
            color='location',
            hover_name='place',
            size_max=60,
            labels={
                'avg_distance': 'Average Distance (m)',
                'avg_monthlyRent': 'Average Monthly Rent (THB)'
            },
            title='Scatter Bubble Plot of Avg Distance vs Avg Monthly Rent'
        )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        location = st.multiselect('ย่าน   ', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())
    with col2:
        place = st.multiselect('สถานที่   ', options=location_df[(location_df['location'].isin(location)) & (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique() if location else location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['place'].unique())
    with col3:
        distance = st.slider('Distance', value=500, min_value=0, max_value=place_agg_df.query('distance < 100000')['distance'].max().astype('int'), step=100)

    if not place and not location:
        place_dis_df = location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())] 
    elif not place:
        place_dis_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['location'].isin(location))]
    elif not location:
        place_dis_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['place'].isin(place))]
    elif location and place:
        place_dis_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                #    (location_df['location'].isin(location)) &
                                (location_df['place'].isin(place))] 

    place_dis_df = place_dis_df[(place_dis_df['distance'] <= distance) & (place_dis_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        total_apartment = st.metric('จำนวนหอพักทั้งหมด', value='{:,.0f}'.format(place_dis_df['apartment_url'].nunique()))
    with col2:
        avg_rental = st.metric('ค่าเช่าเฉลี่ยรายเดือน', value='{:,.2f}'.format(place_dis_df['avgMonthlyRent'].median()))
    with col3:
        avg_sqmtRental = st.metric('ค่าเช่าเฉลี่ยต่อตารางเมตร', value='{:,.2f}'.format(place_dis_df['sqmt_avgMonthlyRent'].median()))
    with col4:
        avg_sqmtArea = st.metric('ตารางเมตรเฉลี่ย', value='{:.2f}'.format((place_dis_df['avgMonthlyRent']/place_dis_df['sqmt_avgMonthlyRent']).median()))

    fig = px.scatter(
        place_dis_df.query('distance < 100000'),
        x='distance',
        y='avgMonthlyRent',
        labels={
            'apartment_url' : 'Apartment URL',
            'distance' : 'Distance',
            'place' : 'Place',
            'avgMonthlyRent' : 'Average Monthly Rent'
        },
        title= 'Distance and Average Monthly Distribution',
        hover_data={'apartment_url': True, 'place': True},
        color='location'
    )
    fig.update_traces(textposition='top center')

    st.plotly_chart(fig, use_container_width=True)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        location = st.multiselect('ย่าน    ', options=location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['location'].unique())
    with col2:
        place = st.multiselect('สถานที่    ', options=location_df[(location_df['location'].isin(location)) & (location_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]['place'].unique() if location else location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())]['place'].unique())
    # with col3:
    #     amen = st.multiselect('สิ่งอำนวยความสะดวก', options=amenities)
    with col3:
        rent = st.slider('ค่าเช่า', value=place_agg_df.query('distance < 100000')['avgMonthlyRent'].median().astype('int'), min_value=0, max_value=place_agg_df.query('distance < 100000')['avgMonthlyRent'].max().astype('int'), step=500)
    with col4:
        distance = st.slider('Distance ', value=500, min_value=0, max_value=place_agg_df.query('distance < 100000')['distance'].max().astype('int'), step=100)
    

    if not place and not location:
        table_info_df = location_df[location_df['apartment_url'].isin(filter_df['apartment_url'].unique())] 
    elif not place:
        table_info_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['location'].isin(location))]
    elif not location:
        table_info_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                (location_df['place'].isin(place))]
    elif location and place:
        table_info_df = location_df[(location_df['apartment_url'].isin(filter_df['apartment_url'].unique())) &
                                #    (location_df['location'].isin(location)) &
                                (location_df['place'].isin(place))] 

    table_info_df = table_info_df[(table_info_df['distance'] <= distance) & 
                                  (table_info_df['avgMonthlyRent'] <= rent) &
                                  (table_info_df['apartment_url'].isin(filter_df['apartment_url'].unique()))]

    st.write('**Infomation Table**')
    table = table_info_df.merge(filter_df[['apartment_url', 'electricity', 'waterFix', 'waterUnit', 'minRoomSize', 'maxRoomSize',
                                           'ac', 'furniture', 'waterHeater', 'fan', 
                                          'carParking', 'wifi', 'cable', 'cctv', 'tv', 'fridge', 'sofa', 'desk', 'stove',
                                          'telephone', 'pet', 'smoking', 'motorbikeParking', 'elevator', 'pool', 'gym', 'keyCard', 
                                          'fingerPrint', 'security', 'restaurant', 'miniMart', 'laundry', 'salon', 'evCharging',]],
                                          on='apartment_url', how='left')

    sorted_table = table[['apartment_url', 'distance', 'avgMonthlyRent', 'avgDailyRent', 'sqmt_avgMonthlyRent',
                          'electricity', 'waterFix', 'waterUnit', 'minRoomSize', 'maxRoomSize',
                          'ac', 'furniture', 'waterHeater', 'fan', 
                          'carParking', 'wifi', 'cable', 'cctv', 'tv', 'fridge', 'sofa', 'desk', 'stove',
                          'telephone', 'pet', 'smoking', 'motorbikeParking', 'elevator',
                          'pool', 'gym', 'keyCard', 'fingerPrint', 'security', 'restaurant', 
                          'miniMart', 'laundry', 'salon', 'evCharging',]].sort_values(by='distance', ascending=True)
    
    # show data in table
    sorted_table
    
    with col5:
        st.markdown("""
        <style>
        div.stDownloadButton > button {
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.download_button(label=f'Export to CSV', 
                           data=sorted_table.to_csv().encode('utf-8'),
                           file_name=f'info_table_{datetime.now().strftime("%Y-%m-%d")}.csv',
                           mime='text/csv')