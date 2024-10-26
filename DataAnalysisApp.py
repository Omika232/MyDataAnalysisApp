import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(page_title= 'data analysis app', page_icon = '📊' )
st.title(':rainbow[Data Analytical portal]')
st.subheader('Explore Data with ease',divider='green')
file= st.file_uploader('Drop csv or excel file',type = ['csv','xlsx'])
if(file != None):
    if (file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File uploaded successfully ',icon= "✔️")

    st.subheader(':rainbow[Basic information of the Dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['Summery','Top and Bottom Rows','Data Type','Columns'])
    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} coloumn in dataset')
        st.subheader(':red[Statical summery of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(f'Top rows')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        botomrows= st.slider('Bottom Rows',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(botomrows))
    with tab3:
        st.subheader('Data Type')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader('Coloumn Name in Dataset')
        st.dataframe(list(data.columns))
    st.subheader('Column Values To Count',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
           column = st.selectbox("Choose Column name", options = list(data.columns))
        with col2:
           toprows = st.number_input('Top Rows',min_value=1,step=1)
        count = st.button('Count')
        if (count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader(':rainbow[Visualization OF DaTaSeT]',divider='rainbow')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_dark')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
    st.subheader(':rainbow[Simplify Your Data by GroupBY]',divider='rainbow')
    st.write('The groupby  sumrize your data by specific categories and group')
    with st.expander('Groupby Data'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column for groupby',options=list(data.columns))
        with col2:
            operation_column = st.selectbox('Choose column for operatioon',options = list(data.columns))
        with col3:
            aggrigation_calculation = st.selectbox('Choose What you want calculate',options = ['sum','max','min','mean','count','median']  )

        if(groupby_cols):
            result1 = data.groupby(groupby_cols).agg(
            newcol = (operation_column,aggrigation_calculation)
            ).reset_index()
            st.dataframe(result1)
            st.subheader(':rainbow[Visualization Of DaTaSeT]',divider='rainbow')
            charts = st.selectbox('Choose Chart for Vizualization',options=['line','bar','pie','scatter','sunburst'])
            if (charts == 'line'):
                x_axis = st.selectbox('Choose x axis',options = list(result1.columns))
                y_axis = st.selectbox('Choose y axis ', options =list(result1.columns) )
                color = st.selectbox('Choose coloumn for information ',options=[None]+list(result1.columns))
                fig1 = px.line(data_frame=result1,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig1)
            elif (charts =='bar'):
                x_axis = st.selectbox('Choose x axis', options=list(result1.columns))
                y_axis = st.selectbox('Choose y axis ', options=list(result1.columns))
                color = st.selectbox('Choose coloumn for information ', options=[None] + list(result1.columns))
                facet_col = st.selectbox('Choose column information',options=[None]+list(result1.columns))
                fig2 = px.bar(data_frame=result1, x=x_axis, y=y_axis, color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig2)
            elif (charts == 'scatter'):
                x_axis = st.selectbox('Choose x axis', options=list(result1.columns))
                y_axis = st.selectbox('Choose y axis ', options=list(result1.columns))
                color = st.selectbox('Choose coloumn for information ', options=[None] + list(result1.columns))
                facet_col = st.selectbox('Choose column information', options=[None] + list(result1.columns))
                size = st.selectbox('Size Column',options=[None]+list(data.columns))
                fig3 = px.scatter(data_frame=result1, x=x_axis, y=y_axis, color=color,size=size,facet_col=facet_col)
                st.plotly_chart(fig3)
            elif (charts=='pie'):
                value = st.selectbox('Choose numeric values', options=list(result1.columns))
                name  = st.selectbox('Choose labels ', options=list(result1.columns))
                fig4= px.pie(data_frame=result1,names=name,values=value)
                st.plotly_chart(fig4)
            elif (charts == 'sunburst'):
                path = st.multiselect('Choose your path ', options=list(result1.columns))
                #value  = this is always our newcol
                fig5 = px.sunburst(data_frame=result1, path=path,values='newcol')
                st.plotly_chart(fig5)

