import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Cell,
    CartesianGrid,
} from 'recharts';

interface DashboardTabProps {
    bookId: string;
}

interface StyleInfluence {
    author: string;
    score: number;
    justification: string;
}

interface ChartData {
    target_reader: Record<string, number>;
    genres: Record<string, number>;
    style_dna: StyleInfluence[];
}

const DashboardTab = ({ bookId }: DashboardTabProps) => {
    const [chartData, setChartData] = useState<ChartData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [animationFrame, setAnimationFrame] = useState<number>(0);

    useEffect(() => {
        const fetchChartData = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/chart/${bookId}`);
                if (!res.ok) throw new Error(`Failed to fetch chart data: ${res.status}`);
                const data = await res.json();
                setChartData(data);
            } catch (err: any) {
                console.error("Error fetching chart data:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchChartData();
    }, [bookId]);

    useEffect(() => {
        if (!chartData) return;

        let frame = 0;
        const totalFrames = 1000;
        const interval = setInterval(() => {
            frame++;
            setAnimationFrame(frame);
            if (frame >= totalFrames) clearInterval(interval);
        }, 40);

        return () => clearInterval(interval);
    }, [chartData]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-64 text-white animate-pulseSlow">
                <p>Generating dashboard...</p>
            </div>
        );
    }

    if (error || !chartData) {
        return (
            <div className="text-white/70">
                <p>Failed to load dashboard visualization.</p>
                <p className="text-red-400">{error}</p>
            </div>
        );
    }

    const renderRadarChart = (title: string, data: Record<string, number>, color: string) => {
        const labels = Object.keys(data);
        const values = Object.values(data);
        const progress = Math.min(animationFrame / 30, 1);
        const animatedValues = values.map(v => v * progress);

        const closedValues = [...animatedValues, animatedValues[0]];
        const closedLabels = [...labels, labels[0]];

        return (
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 shadow-2xl">
                <h3 className="text-2xl font-semibold mb-6 text-white text-center">{title}</h3>
                <Plot
                    data={[
                        {
                            type: "scatterpolar",
                            r: closedValues,
                            theta: closedLabels,
                            fill: "toself",
                            mode: "lines+markers",
                            line: { color: color, width: 3 },
                            marker: { color: color, size: 6 },
                            fillcolor: `${color}33`,
                        }
                    ]}
                    layout={{
                        font: {
                            family: "Poppins, sans-serif",
                            color: "white"
                        },
                        polar: {
                            bgcolor: "transparent",
                            radialaxis: {
                                visible: true,
                                range: [0, 100],
                                gridcolor: "light-grey",
                                linecolor: "#6b7280",
                                tickfont: { color: "#e0e7ff" },
                            },
                            angularaxis: {
                                tickfont: { color: "#e0e7ff" },
                                gridcolor: "#6b728080",
                            }
                        },
                        showlegend: false,
                        paper_bgcolor: "transparent",
                        plot_bgcolor: "transparent",
                        margin: { t: 30, l: 30, r: 30, b: 30 },
                    }}
                    style={{ width: "100%", height: "500px" }}
                    config={{ displayModeBar: false }}
                />
            </div>
        );
    };

    const renderGenreBarChart = (title: string, data: Record<string, number>, color: string = "#e879f9") => {
        const progress = Math.min(animationFrame / 30, 1);
        const chartData = Object.entries(data).map(([genre, value]) => ({
            genre,
            value: value * progress,
        }));

        return (
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 shadow-2xl">
                <h3 className="text-2xl font-semibold mb-6 text-white text-center">{title}</h3>
                <ResponsiveContainer width="100%" height={chartData.length * 40 + 100}>
                    <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 10, right: 30, left: 50, bottom: 30 }}
                        barCategoryGap="20%"
                    >
                        <CartesianGrid stroke="#6b7280" strokeDasharray="3 3" />
                        <XAxis
                            type="number"
                            domain={[0, 100]}
                            tick={{ fill: '#e0e7ff', fontFamily: 'Poppins' }}
                            stroke="#6b7280"
                            tickLine={{ stroke: "#6b7280" }}
                            axisLine={{ stroke: "#6b7280" }}
                        />
                        <YAxis
                            type="category"
                            dataKey="genre"
                            tick={{ fill: '#e0e7ff', fontFamily: 'Poppins' }}
                            width={200}
                            stroke="#6b7280"
                            tickLine={false}
                        />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.1)' }}
                            contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                            labelStyle={{ color: 'white' }}
                            itemStyle={{ color: 'white' }}
                        />
                        <Bar
                            dataKey="value"
                            radius={[4, 4, 4, 4]}
                            animationDuration={600}
                        >
                            {chartData.map((_, index) => (
                                <Cell key={`cell-${index}`} fill={color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    };

    const renderStyleDnaBarChart = (title: string, data: StyleInfluence[], color: string = "#facc15") => {
        const progress = Math.min(animationFrame / 30, 1);
        const chartData = data.map(item => ({
            author: item.author,
            value: item.score * progress,
            justification: item.justification,
        }));

        return (
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 shadow-2xl space-y-6">
                <h3 className="text-2xl font-semibold text-white text-center">{title}</h3>
                <ResponsiveContainer width="100%" height={chartData.length * 40 + 100}>
                    <BarChart
                        data={chartData}
                        layout="vertical"
                        margin={{ top: 10, right: 30, left: 50, bottom: 30 }}
                        barCategoryGap="10%"
                    >
                        <CartesianGrid stroke="#6b7280" strokeDasharray="3 3" />
                        <XAxis
                            type="number"
                            domain={[0, 100]}
                            tick={{ fill: '#e0e7ff', fontFamily: 'Poppins' }}
                            stroke="#6b7280"
                            tickLine={{ stroke: "#6b7280" }}
                            axisLine={{ stroke: "#6b7280" }}
                        />
                        <YAxis
                            type="category"
                            dataKey="author"
                            tick={{ fill: '#e0e7ff', fontFamily: 'Poppins' }}
                            width={200}
                            stroke="#6b7280"
                            tickLine={false}
                        />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.1)' }}
                            content={({ payload }) => {
                                if (!payload || !payload.length) return null;
                                const { author, justification } = payload[0].payload;
                                return (
                                    <div className="p-4 bg-gray-800 text-white rounded-md max-w-sm text-sm">
                                        <p className="font-bold mb-2">{author}</p>
                                        <p>{justification}</p>
                                    </div>
                                );
                            }}
                        />
                        <Bar dataKey="value" radius={[4, 4, 4, 4]} animationDuration={600}>
                            {chartData.map((_, index) => (
                                <Cell key={`cell-${index}`} fill={color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>

                {/* Animated Notes */}
                <div className="text-white/80 mt-8 space-y-4 transition-all duration-700 ease-out animate-fadeIn">
                    <h4 className="text-xl font-semibold">Stylistic Notes</h4>
                    {chartData.map(({ author, justification }, index) => (
                        <div
                            key={author}
                            className="border-l-4 border-yellow-400 pl-4 opacity-0 animate-fadeIn"
                            style={{ animationDelay: `${index * 100}ms`, animationFillMode: "forwards" }}
                        >
                            <p className="font-medium text-yellow-300">{author}</p>
                            <p className="text-sm">{justification}</p>
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    return (
        <div className="space-y-10 animate-fadeIn">
            {renderRadarChart("Target Reader Segmentation", chartData.target_reader, "#38bdf8")}
            {renderGenreBarChart("Genre Classification", chartData.genres)}
            {renderStyleDnaBarChart("Style DNA Breakdown", chartData.style_dna)}
        </div>
    );
};

export default DashboardTab;
