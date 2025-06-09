const subscriptionKey = import.meta.env.VITE_SUBSCRIPTION_KEY;

let map, features = [];

function init() {
    fetch("https://example.com/gps-data.json") // Replace with real JSON if needed
        .then(res => res.json())
        .then(gps => {
            features.push(new atlas.data.Feature(
                new atlas.data.Point([parseFloat(gps.gps.lon), parseFloat(gps.gps.lat)])
            ));
        })
        .then(() => {
            map = new atlas.Map("myMap", {
                center: [-122.26473, 47.73444],
                zoom: 14,
                authOptions: {
                    authType: "subscriptionKey",
                    subscriptionKey: subscriptionKey,
                },
            });

            map.events.add("ready", function () {
                const source = new atlas.source.DataSource();
                map.sources.add(source);
                map.layers.add(new atlas.layer.BubbleLayer(source));
                source.add(features);
            });
        });
}
