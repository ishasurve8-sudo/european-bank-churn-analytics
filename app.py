import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="European Bank Churn Analytics", page_icon="🏦", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("European_Bank__1_.csv")
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,45,60,100], labels=['Under 30','30 to 45','46 to 60','Above 60'])
    df['BalanceSegment'] = pd.cut(df['Balance'], bins=[-1,0,50000,999999], labels=['Zero Balance','Low Balance','High Balance'])
    df['CreditBand'] = pd.cut(df['CreditScore'], bins=[0,580,670,740,850], labels=['Poor','Fair','Good','Excellent'])
    df['TenureGroup'] = pd.cut(df['Tenure'], bins=[-1,2,5,10], labels=['New','Mid-term','Long-term'])
    return df

df = load_data()

st.sidebar.title("🔍 Filter Customers")
selected_geo = st.sidebar.multiselect("Select Country", options=df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_active = st.sidebar.multiselect("Member Status", options=[0,1], format_func=lambda x: "Active" if x==1 else "Inactive", default=[0,1])

filtered_df = df[(df['Geography'].isin(selected_geo)) & (df['Gender'].isin(selected_gender)) & (df['IsActiveMember'].isin(selected_active))]

st.title("🏦 European Bank — Customer Churn Analytics")
st.caption("Customer Segmentation & Retention Intelligence · 10,000 Records · 2025")
st.markdown("---")

total = len(filtered_df)
churned = int(filtered_df['Exited'].sum())
retained = total - churned
churn_pct = churned / total * 100 if total > 0 else 0
hv_df = filtered_df[filtered_df['Balance'] > 100000]
hv_churn_pct = hv_df['Exited'].mean() * 100 if len(hv_df) > 0 else 0
inactive_df = filtered_df[filtered_df['IsActiveMember'] == 0]
inactive_churn_pct = inactive_df['Exited'].mean() * 100 if len(inactive_df) > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{total:,}")
col2.metric("Churned", f"{churned:,}")
col3.metric("Churn Rate", f"{churn_pct:.1f}%")
col4.metric("High-Value Churn", f"{hv_churn_pct:.1f}%")
col5.metric("Inactive Churn", f"{inactive_churn_pct:.1f}%")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview","🌍 Geography","👥 Demographics","💰 Financial Profile","💎 High-Value Customers"])

with tab1:
    st.subheader("Overall Churn Summary")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(values=[churned, retained], names=['Churned','Retained'], hole=0.6, color_discrete_sequence=['#ef4444','#22c55e'], title="Churn vs Retention")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        prod = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
        prod.columns = ['Number of Products','Churn Rate']
        fig2 = px.bar(prod, x='Number of Products', y='Churn Rate', title="Churn Rate by Number of Products", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.0%')
        fig2.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig2, use_container_width=True)
    all_seg = pd.DataFrame({'Segment':['France','Germany','Spain','Under 30','30-45','46-60','60+','Female','Male','Active','Inactive'],'Churn Rate':[0.162,0.324,0.167,0.075,0.157,0.511,0.248,0.251,0.165,0.143,0.269]})
    fig3 = px.bar(all_seg, x='Segment', y='Churn Rate', title="Segment-wise Churn Comparison", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.0%')
    fig3.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Geographic Churn Analysis")
    geo = filtered_df.groupby('Geography')['Exited'].mean().reset_index()
    geo.columns = ['Country','Churn Rate']
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(geo, x='Country', y='Churn Rate', title="Churn Rate by Country", color='Country', color_discrete_map={'France':'#3b82f6','Germany':'#ef4444','Spain':'#f59e0b'}, text_auto='.1%')
        fig.update_layout(yaxis_tickformat='.0%', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        geo_gender = filtered_df.groupby(['Geography','Gender'])['Exited'].mean().reset_index()
        geo_gender.columns = ['Country','Gender','Churn Rate']
        fig2 = px.bar(geo_gender, x='Country', y='Churn Rate', color='Gender', barmode='group', title="Churn by Country and Gender", color_discrete_map={'Female':'#a855f7','Male':'#3b82f6'}, text_auto='.1%')
        fig2.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig2, use_container_width=True)
    geo_detail = filtered_df.groupby('Geography').agg(Total=('Exited','count'), Churned=('Exited','sum')).reset_index()
    geo_detail['Customer Share %'] = geo_detail['Total'] / geo_detail['Total'].sum() * 100
    geo_detail['Churn Share %'] = geo_detail['Churned'] / geo_detail['Churned'].sum() * 100
    fig3 = px.bar(geo_detail.melt(id_vars='Geography', value_vars=['Customer Share %','Churn Share %']), x='Geography', y='value', color='variable', barmode='group', title="Customer Share vs Churn Contribution (%)", text_auto='.1f')
    fig3.update_layout(yaxis_title="Percentage (%)", legend_title="")
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Demographic Churn Patterns")
    col1, col2 = st.columns(2)
    with col1:
        age = filtered_df.groupby('AgeGroup', observed=True)['Exited'].mean().reset_index()
        age.columns = ['Age Group','Churn Rate']
        fig = px.bar(age, x='Age Group', y='Churn Rate', title="Churn Rate by Age Group", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.1%')
        fig.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        gender = filtered_df.groupby('Gender')['Exited'].mean().reset_index()
        gender.columns = ['Gender','Churn Rate']
        fig2 = px.bar(gender, x='Churn Rate', y='Gender', orientation='h', title="Churn Rate by Gender", color='Gender', color_discrete_map={'Female':'#a855f7','Male':'#3b82f6'}, text_auto='.1%')
        fig2.update_layout(xaxis_tickformat='.0%', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    col3, col4 = st.columns(2)
    with col3:
        tenure = filtered_df.groupby('TenureGroup', observed=True)['Exited'].mean().reset_index()
        tenure.columns = ['Tenure Group','Churn Rate']
        fig3 = px.bar(tenure, x='Tenure Group', y='Churn Rate', title="Churn Rate by Tenure", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.1%')
        fig3.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        active = filtered_df.groupby('IsActiveMember')['Exited'].mean().reset_index()
        active['Status'] = active['IsActiveMember'].map({0:'Inactive',1:'Active'})
        fig4 = px.bar(active, x='Status', y='Exited', title="Active vs Inactive Member Churn", color='Status', color_discrete_map={'Active':'#22c55e','Inactive':'#ef4444'}, text_auto='.1%')
        fig4.update_layout(yaxis_tickformat='.0%', showlegend=False, yaxis_title='Churn Rate')
        st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.subheader("Financial Profile & Churn Behaviour")
    col1, col2 = st.columns(2)
    with col1:
        bal = filtered_df.groupby('BalanceSegment', observed=True)['Exited'].mean().reset_index()
        bal.columns = ['Balance Segment','Churn Rate']
        fig = px.bar(bal, x='Balance Segment', y='Churn Rate', title="Churn by Account Balance", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.1%')
        fig.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        credit = filtered_df.groupby('CreditBand', observed=True)['Exited'].mean().reset_index()
        credit.columns = ['Credit Band','Churn Rate']
        fig2 = px.bar(credit, x='Credit Band', y='Churn Rate', title="Churn by Credit Score Band", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.1%')
        fig2.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig2, use_container_width=True)
    prod = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    prod.columns = ['Number of Products','Churn Rate']
    fig3 = px.bar(prod, x='Number of Products', y='Churn Rate', title="Product Holding vs Churn", color='Churn Rate', color_continuous_scale='RdYlGn_r', text_auto='.1%')
    fig3.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig3, use_container_width=True)

with tab5:
    st.subheader("High-Value Customer Churn (Balance > €100,000)")
    hv_total = len(hv_df)
    hv_exited = int(hv_df['Exited'].sum())
    hv_rate = hv_df['Exited'].mean() * 100 if hv_total > 0 else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("HV Customers", f"{hv_total:,}")
    c2.metric("HV Churned", f"{hv_exited:,}")
    c3.metric("HV Churn Rate", f"{hv_rate:.1f}%")
    col1, col2 = st.columns(2)
    with col1:
        hv_geo = hv_df.groupby('Geography')['Exited'].mean().reset_index()
        hv_geo.columns = ['Country','Churn Rate']
        fig = px.bar(hv_geo, x='Country', y='Churn Rate', title="High-Value Churn by Country", color='Country', color_discrete_map={'France':'#3b82f6','Germany':'#ef4444','Spain':'#f59e0b'}, text_auto='.1%')
        fig.update_layout(yaxis_tickformat='.0%', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        compare = pd.DataFrame({'Country':['France','Germany','Spain'],'Overall':[0.162,0.324,0.167],'High-Value':[0.180,0.359,0.175]})
        fig2 = px.bar(compare.melt(id_vars='Country', var_name='Customer Type', value_name='Churn Rate'), x='Country', y='Churn Rate', color='Customer Type', barmode='group', title="Overall vs High-Value Churn", color_discrete_map={'Overall':'#3b82f6','High-Value':'#a855f7'}, text_auto='.1%')
        fig2.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### 📋 High-Value Customer Data Table")
    st.dataframe(hv_df[['Geography','Gender','Age','Balance','CreditScore','NumOfProducts','IsActiveMember','Exited']].sort_values('Balance', ascending=False).head(50), use_container_width=True)
    