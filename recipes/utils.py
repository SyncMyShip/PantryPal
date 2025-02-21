from io import BytesIO
import base64
import matplotlib.pyplot as plt
from recipes.models import Recipe

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(5, 3))

    if chart_type == '#1':  # Bar chart
        plt.bar(data['name'], data['cooking_time'])
        plt.xlabel('Recipe Name')
        plt.ylabel('Cooking Time (min)')
        plt.title('Cook Time by Recipe')

    elif chart_type == '#2':  # Pie chart
        labels = kwargs.get('labels')
        values = kwargs.get('values')

        if labels is None or values is None:
            print("Labels or values are not provided for the pie chart.")
            return None

        print("Labels:", labels)
        print("Values:", values)

        # Convert values to float and filter non-numeric
        numeric_values = []
        for v in values:
            try:
                numeric_values.append(float(v))
            except ValueError:
                print(f"Skipping non-numeric value: {v}")

        if not numeric_values:
            print("No valid numeric values provided for the pie chart.")
            return None

        if len(numeric_values) != len(labels):
            print("Mismatch between number of numeric values and labels.")
            return None

        plt.pie(numeric_values, labels=labels, autopct='%1.1f%%')
        plt.title('Difficulty')

    elif chart_type == '#3':  # Line chart
        plt.plot(data['name'], data['cooking_time'])
        plt.xlabel('Recipe Name')
        plt.ylabel('Cooking Time (min)')
        plt.title('Cook Time by Recipe')

    else:
        print('Invalid chart type')
        return None

    plt.tight_layout()
    return get_graph()

def get_graph():
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    chart_image = base64.b64encode(buf.read()).decode('utf-8')
    return chart_image
