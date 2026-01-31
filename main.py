import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from db import get_data
import pandas as pd


def configure_page():
    st.set_page_config(
        page_title="Olist E-Commerce Dashboard",
        page_icon="🛒",
        layout="wide"
    )


def main():
    configure_page()
    
    st.title("🛒 Olist E-Commerce Dashboard")
    st.markdown("### Brazilian E-Commerce Analysis (2016-2018)")
    
    st.sidebar.header("📊 Фильтры")
    
    try:
        revenue_df = get_data('revenue_by_month')
        categories_df = get_data('top_categories')
        states_df = get_data('sales_by_state')
        payments_df = get_data('payment_methods')
        satisfaction_df = get_data('customer_satisfaction')
        
        if not states_df.empty and 'state' in states_df.columns:
            all_states = ['All'] + sorted(states_df['state'].unique().tolist())
            selected_state = st.sidebar.selectbox(
                "Select State",
                options=all_states
            )
        else:
            selected_state = 'All'
        
        # Фильтры данных
        if selected_state != 'All':
            if not revenue_df.empty and 'state' in revenue_df.columns:
                revenue_df = revenue_df[revenue_df['state'] == selected_state]
            if not categories_df.empty and 'state' in categories_df.columns:
                categories_df = categories_df[categories_df['state'] == selected_state]
            if not states_df.empty and 'state' in states_df.columns:
                states_df = states_df[states_df['state'] == selected_state]
            if not payments_df.empty and 'state' in payments_df.columns:
                payments_df = payments_df[payments_df['state'] == selected_state]
            if not satisfaction_df.empty and 'state' in satisfaction_df.columns:
                satisfaction_df = satisfaction_df[satisfaction_df['state'] == selected_state]
        
        # Фильтр по месяцам
        if not revenue_df.empty and 'month' in revenue_df.columns:
            all_months = sorted(revenue_df['month'].unique())
            selected_months = st.sidebar.multiselect(
                "Select Month Range",
                options=all_months,
                default=all_months
            )
            
            if selected_months:
                revenue_df = revenue_df[revenue_df['month'].isin(selected_months)]
                if not categories_df.empty and 'month' in categories_df.columns:
                    categories_df = categories_df[categories_df['month'].isin(selected_months)]
                if not payments_df.empty and 'month' in payments_df.columns:
                    payments_df = payments_df[payments_df['month'].isin(selected_months)]
                if not satisfaction_df.empty and 'month' in satisfaction_df.columns:
                    satisfaction_df = satisfaction_df[satisfaction_df['month'].isin(selected_months)]
        
        # Агрегация данных для отображения
        if not revenue_df.empty:
            revenue_display = revenue_df.groupby('month').agg({
                'total_orders': 'sum',
                'monthly_revenue': 'sum',
                'avg_order_value': 'mean'
            }).reset_index()
        else:
            revenue_display = revenue_df
            
        if not categories_df.empty:
            categories_display = categories_df.groupby('category').agg({
                'order_count': 'sum',
                'total_revenue': 'sum',
                'avg_price': 'mean',
                'unique_products': 'sum'
            }).reset_index().sort_values('total_revenue', ascending=False).head(10)
        else:
            categories_display = categories_df
            
        if not payments_df.empty:
            payments_display = payments_df.groupby('payment_method').agg({
                'order_count': 'sum',
                'total_value': 'sum',
                'avg_payment': 'mean'
            }).reset_index().sort_values('order_count', ascending=False)
        else:
            payments_display = payments_df
            
        if not satisfaction_df.empty:
            satisfaction_display = satisfaction_df.groupby('review_score').agg({
                'order_count': 'sum',
                'avg_order_value': 'mean',
                'avg_delivery_days': 'mean'
            }).reset_index()
        else:
            satisfaction_display = satisfaction_df
        
        # Метрики вверху
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = revenue_display['monthly_revenue'].sum() if not revenue_display.empty else 0
            st.metric("Общая выручка", f"R$ {total_revenue:,.2f}")
        
        with col2:
            total_orders = revenue_display['total_orders'].sum() if not revenue_display.empty else 0
            st.metric("Всего заказов", f"{int(total_orders):,}")
        
        with col3:
            avg_order = revenue_display['avg_order_value'].mean() if not revenue_display.empty else 0
            st.metric("Средний чек", f"R$ {avg_order:.2f}")
        
        with col4:
            avg_score = satisfaction_display['review_score'].mean() if not satisfaction_display.empty else 0
            st.metric("Средняя оценка", f"{avg_score:.1f}/5.0")
        
        st.markdown("---")
        
        # Строка 1: Месячная выручка и Топ категории
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Месячная выручка")
            if not revenue_display.empty:
                fig = px.line(
                    revenue_display,
                    x='month',
                    y='monthly_revenue',
                    title='Выручка по месяцам',
                    labels={'monthly_revenue': 'Выручка $', 'month': 'Месяц'}
                )
                fig.update_traces(line_color='#1f77b4', line_width=3)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет данных по выручке")
        
        with col2:
            st.subheader("🏆 Топ категории")
            if not categories_display.empty:
                fig = px.bar(
                    categories_display,
                    x='total_revenue',
                    y='category',
                    orientation='h',
                    title='Топ 10 категорий по выручке',
                    labels={'total_revenue': 'Выручка $', 'category': 'Категория'}
                )
                fig.update_traces(marker_color='#2ca02c')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет данных по категориям")
        
        st.markdown("---")
        
        # Строка 2: Продажи по штатам и Способы оплаты
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Продажи по штатам")
            if not states_df.empty:
                fig = px.bar(
                    states_df.head(15),
                    x='state',
                    y='total_revenue',
                    title='Топ 15 штатов по выручке',
                    labels={'total_revenue': 'Выручка $', 'state': 'Штат'},
                    color='total_revenue',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет данных по штатам")
        
        with col2:
            st.subheader("💳 Способы оплаты")
            if not payments_display.empty:
                fig = px.pie(
                    payments_display,
                    values='order_count',
                    names='payment_method',
                    title='Распределение способов оплаты'
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет данных по способам оплаты")
        
        st.markdown("---")
        
        # Строка 3: Удовлетворенность клиентов
        st.subheader("⭐ Отзывы клиентов и удовлетворенность")
        if not satisfaction_display.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    satisfaction_display,
                    x='review_score',
                    y='order_count',
                    title='Распределение оценок отзывов',
                    labels={'order_count': 'Количество заказов', 'review_score': 'Оценка отзыва'},
                    color='review_score',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    satisfaction_display,
                    x='review_score',
                    y='avg_delivery_days',
                    title='Среднее время доставки по оценке отзыва',
                    labels={'avg_delivery_days': 'Дни доставки', 'review_score': 'Оценка отзыва'},
                    color='avg_delivery_days',
                    color_continuous_scale='Reds_r'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Нет данных по удовлетворенности клиентов")
        
        # Футер
        st.markdown("---")
        st.markdown("**Data Source:** Olist Brazilian E-Commerce Dataset (2016-2018)")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Make sure to run ddl.py first to create and populate the database!")


if __name__ == "__main__":
    main()