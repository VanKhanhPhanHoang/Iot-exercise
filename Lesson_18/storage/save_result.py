def save_result(fruit, ripeness, filepath="results.csv"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filepath, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now, fruit, ripeness])
    print(f"[Storage] Result saved: {fruit} - {ripeness}")
