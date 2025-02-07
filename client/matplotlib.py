import matplotlib.pyplot as plt
import numpy as np
from django.http import JsonResponse

def test(request):
    response_data = {}

    # 2️⃣ Basic Plots Examples
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 25, 30, 40]
    
    plt.figure()
    plt.plot(x, y)  # Line chart
    plt.savefig("line_chart.png")
    response_data["line_chart"] = "line_chart.png"
    plt.close()
    
    plt.figure()
    plt.bar(x, y)  # Bar chart
    plt.savefig("bar_chart.png")
    response_data["bar_chart"] = "bar_chart.png"
    plt.close()
    
    plt.figure()
    plt.scatter(x, y)  # Scatter plot
    plt.savefig("scatter_plot.png")
    response_data["scatter_plot"] = "scatter_plot.png"
    plt.close()
    
    data = np.random.randn(1000)
    plt.figure()
    plt.hist(data, bins=20)  # Histogram
    plt.savefig("histogram.png")
    response_data["histogram"] = "histogram.png"
    plt.close()

    
    # 3️⃣ Graph Customization Examples
    plt.figure()
    plt.plot(x, y, label="Line Graph", color="red", linestyle="--")
    plt.title("Customized Graph")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.legend()
    plt.grid(True)
    plt.savefig("customized_graph.png")
    response_data["customized_graph"] = "customized_graph.png"
    plt.close()

    
    # 4️⃣ Multiple Subplots Example
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(x, y, color="blue")
    plt.title("Line Graph")
    
    plt.subplot(1, 2, 2)
    plt.bar(x, y, color="green")
    plt.title("Bar Graph")
    
    plt.savefig("multiple_plots.png")
    response_data["multiple_plots"] = "multiple_plots.png"
    plt.close()

    
    # 5️⃣ Saving Graph as Image Example
    plt.figure()
    plt.plot(x, y)
    plt.savefig("saved_graph.png")
    response_data["saved_graph"] = "saved_graph.png"
    plt.close()

    
    # 6️⃣ Special Plot Types Examples
    plt.figure()
    plt.fill_between(x, np.array(y) - 5, np.array(y) + 5, color="gray", alpha=0.5)
    plt.plot(x, y, color="black")
    plt.savefig("fill_between_plot.png")
    response_data["fill_between_plot"] = "fill_between_plot.png"
    plt.close()
    
    return JsonResponse(response_data)
