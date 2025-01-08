function App() {
    const [priceData] = React.useState({
        timestamp: new Date().toLocaleTimeString(),
        sol_amount: 0.28743368,
        sol_price: 196.18,
        pool_value: 56.39
    });

    return (
        <div className="min-h-screen bg-black p-8 font-mono">
            <div className="max-w-3xl mx-auto">
                <div className="bg-black border border-green-500 p-4 rounded">
                    <div className="flex items-center mb-4">
                        <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500 mr-2"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    </div>
                    
                    <div className="text-green-500">
                        <p className="text-xl mb-4">$ solana-price-tracker --status</p>
                        
                        <p className="mb-2">
                            [<span className="text-yellow-500">{priceData.timestamp}</span>] System online...
                        </p>
                        
                        <div className="mt-4">
                            <p>>>> SOL STATUS</p>
                            <p className="ml-4">Price: <span className="text-yellow-500">${priceData.sol_price.toFixed(2)}</span></p>
                            <p className="ml-4">Pool Amount: <span className="text-yellow-500">{priceData.sol_amount.toFixed(8)}</span></p>
                            <p className="ml-4">Pool Value: <span className="text-yellow-500">${priceData.pool_value.toFixed(2)}</span></p>
                        </div>
                        
                        <div className="mt-4">
                            <p className="blink">█</p>
                        </div>
                    </div>
                </div>
            </div>
            <style>{`
                @keyframes blink {
                    0% { opacity: 0; }
                    50% { opacity: 1; }
                    100% { opacity: 0; }
                }
                .blink {
                    animation: blink 1s infinite;
                }
            `}</style>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
