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

const UnitsChart: React.FC<ChartProps> = ({ data }) => {
    const sortedPreds = [...data.preds].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const sortedPicks = [...data.picks].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    const chartData = sortedPreds.map((pred, index) => ({
        date: pred.date,
        predsUnits: (pred.allTime.units).toFixed(2),
        picksUnits: (sortedPicks[index]?.allTime.units).toFixed(2)|| '0',
    }))
    const allUnits = chartData.flatMap(d => [parseFloat(d.predsUnits), parseFloat(d.picksUnits)])
    const minY = Math.floor(Math.min(...allUnits) - 5)
    const maxY = Math.ceil(Math.max(...allUnits) + 5)
    const domain = [minY, maxY]
    return (
        <div style={{ width: "100%", height: 500, marginTop: '30px' }}>
            <h2 style={{ textAlign: "center" }}>Units Won</h2>
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
                        domain={domain}
                        label={{
                            value: "Units",
                            angle: -90,
                            position: "insideLeft"
                        }}
                    />
                    <Tooltip />
                    <Legend
                        verticalAlign="top"
                        formatter={(value) => 
                            value === "predsUnits"
                            ? "Prediction Units"
                            : "Pick Units"
                        }
                    />
                    <Line
                        type="monotone"
                        dataKey="predsUnits"
                        stroke="#8884d8"
                        activeDot={{ r: 8 }}
                    />
                    <Line
                        type="monotone"
                        dataKey="picksUnits"
                        stroke="#82ca9d"
                        activeDot={{ r: 8 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}

export default UnitsChart