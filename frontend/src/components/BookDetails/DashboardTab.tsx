import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

interface DashboardTabProps {
    bookId: string;
}

const DashboardTab = ({ bookId }: DashboardTabProps) => {
    const [audienceScores, setAudienceScores] = useState<Record<string, number> | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [animationFrame, setAnimationFrame] = useState<number>(0);

    useEffect(() => {
        const fetchAudienceScores = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/spider-chart/${bookId}`);
                if (!res.ok) {
                    throw new Error(`Failed to fetch audience scores: ${res.status}`);
                }
                const data = await res.json();
                setAudienceScores(data);
            } catch (err: any) {
                console.error("Error fetching audience scores:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAudienceScores();
    }, [bookId]);

    useEffect(() => {
        if (!audienceScores) return;

        let frame = 0;
        const totalFrames = 1000; // controls animation smoothness
        const interval = setInterval(() => {
            frame++;
            setAnimationFrame(frame);
            if (frame >= totalFrames) {
                clearInterval(interval);
            }
        }, 40); // 20ms between frames (~600ms total)

        return () => clearInterval(interval);
    }, [audienceScores]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-64 text-white animate-pulseSlow">
                <p>Generating dashboard...</p>
            </div>
        );
    }

    if (error || !audienceScores) {
        return (
            <div className="text-white/70">
                <p>Failed to load dashboard visualization.</p>
                <p className="text-red-400">{error}</p>
            </div>
        );
    }

    const labels = Object.keys(audienceScores);
    const finalValues = Object.values(audienceScores);
    const progress = Math.min(animationFrame / 30, 1); // 0 to 1
    const animatedValues = finalValues.map(v => v * progress);

    const closedAnimatedValues = [...animatedValues, animatedValues[0]];
    const closedLabels = [...labels, labels[0]];

    return (
        <div className="space-y-6 animate-fadeIn">
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 shadow-2xl">
                <h3 className="text-2xl font-semibold mb-6 text-white text-center">Target Reader Segmentation</h3>
                <Plot
                    data={[
                        {
                            type: "scatterpolar",
                            r: closedAnimatedValues,
                            theta: closedLabels,
                            fill: "toself",
                            mode: "lines+markers",
                            line: { color: "#38bdf8", width: 3 },
                            marker: { color: "#38bdf8", size: 6 },
                            fillcolor: "rgba(56, 189, 248, 0.2)",
                            // fillcolor: "rgba(232, 119, 243, 0.41)",
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
                                // linecolor: "#93c5fd",
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
        </div>
    );
};

export default DashboardTab;
