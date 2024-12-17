import React from 'react'
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts"

type Record = {
    percentage: number,
    correct: number,
    total: number,
    units: number
}

type ChartProps = {
    data: {
        preds: Array<{ date: string, today: Record, allTime: Record }>,
        picks: Array<{ date: string, today: Record, allTime: Record }>
    }
}

const WinPercentageChart: React.FC<ChartProps> = ({ data }) => {
    const sortedPreds = [...data.preds].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const sortedPicks = [...data.picks].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const chartData = sortedPreds.map((pred, index) => ({
        date: pred.date,
        predsPercentage: (pred.allTime.percentage * 100).toFixed(2),
        picksPercentage: (sortedPicks[index]?.allTime.percentage * 100).toFixed(2) || 0,
    }))
    return (
        <div style={{ width: "100%", height: 500 }}>
            <h2 style={{ textAlign: "center", marginTop: '40px' }}>Win Percentage</h2>
            <ResponsiveContainer width="95%" height="100%">
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="date"
                        label={{
                            value: "Date",
                            position: "insideBottom",
                            offset: -5
                        }}
                    />
                    <YAxis
                        domain={[0, 100]}
                        label={{
                            value: "Percentage(%)",
                            angle: -90,
                            position: "insideLeft"
                        }}
                    />
                    <Tooltip />
                    <Legend
                        verticalAlign="top"
                        formatter={(value) => 
                            value === "predsPercentage"
                            ? "Prediction Accuracy"
                            : "Pick Accuracy"
                        }
                    />
                    <Line
                        type="monotone"
                        dataKey="predsPercentage"
                        stroke="#8884d8"
                        activeDot={{ r: 8 }}
                    />
                    <Line
                        type="monotone"
                        dataKey="picksPercentage"
                        stroke="#82ca9d"
                        activeDot={{ r: 8 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}

export default WinPercentageChart