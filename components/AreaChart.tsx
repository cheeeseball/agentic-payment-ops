"use client";

import { useEffect, useState } from "react";
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Filler
);

export default function AreaChart() {
    // 👉 PUT IT HERE (inside component, before data)
    const [points, setPoints] = useState<number[]>(generateRandomData(30));

    useEffect(() => {
        const interval = setInterval(() => {
            setPoints((prev) => {
                const next = [...prev.slice(1)];
                const last = prev[prev.length - 1];
                next.push(last + Math.random() * 0.5 - 0.2);
                return next;
            });
        }, 6000);

        return () => clearInterval(interval);
    }, []);

    const data = {
        labels: points.map((_, i) => i.toString()),
        datasets: [
            {
                data: points,
                borderColor: "green",
                backgroundColor: "rgba(0, 200, 0, 0.2)",
                fill: true,
                tension: 0.1,
                pointRadius: 0,
            },
        ],
    };

    const options = {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            x: { display: false },
            y: { display: false },
        },
        plugins: {
            legend: { display: false },
        },
    };

    return (
        <div className="w-screen h-full">
            <Line data={data} options={options} />
        </div>
    );
}

function generateRandomData(n: number) {
    let value = 50;
    return Array.from({ length: n }, () => {
        value += Math.random() * 10 - 5;
        return Math.max(10, value);
    });
}
