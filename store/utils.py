# analytics/utils.py

from .models import Orders
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def get_sales_data(timeframe='daily'):
    if timeframe == 'daily':
        start_date = timezone.now() - timedelta(days=1)
    elif timeframe == 'weekly':
        start_date = timezone.now() - timedelta(weeks=1)
    elif timeframe == 'monthly':
        start_date = timezone.now() - timedelta(weeks=4)
    else:
        raise ValueError("Invalid timeframe")

    sales_data = (
        Orders.objects.filter(created_at__gte=start_date)
        .values('created_at__date')
        .annotate(total_sales=Sum('amount'), total_quantity=Sum('quantity'))
        .order_by('created_at__date')
    )

    return list(sales_data)

# analytics/utils.py

from .models import Orders
from django.db.models import Sum
from django.utils import timezone

def get_historical_sales_data():
    # Fetch historical order data
    sales_data = Orders.objects.values('created_at__date').annotate(
        total_sales=Sum('amount')
    ).order_by('created_at__date')

    # Convert the QuerySet to a DataFrame
    import pandas as pd
    df = pd.DataFrame(list(sales_data))
    df['created_at__date'] = pd.to_datetime(df['created_at__date'])
    df.set_index('created_at__date', inplace=True)

    return df


from sklearn.linear_model import LinearRegression
import numpy as np

def train_sales_model(df):
    # Preparing data for Linear Regression
    df['days'] = (df.index - df.index.min()).days
    X = df['days'].values.reshape(-1, 1)
    y = df['total_sales'].values

    model = LinearRegression()
    model.fit(X, y)

    return model
