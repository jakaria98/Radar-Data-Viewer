import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";
import RadarAnimation from "../Components/RadarAnimation";

const LoginPage = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [message, setMessage] = useState("");
	const navigate = useNavigate();
	const { authState, setAuthState } = useAuth();

	useEffect(() => {
		if (authState.isLoggedIn) {
			navigate("/home");
		}
	}, [authState.isLoggedIn, navigate]);

	const handleLogin = async (e) => {
        e.preventDefault();
        if (!username || !password) {
            setMessage('Please enter both username and password.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setMessage('Login successful!');
                console.log('Response:', data);

                // Extract the token and other user details from the response
                const token = data.token;
                const hasAdminStatus = data?.user?.is_staff ? true : false;

                // Save the token and user info in the auth state
                setAuthState({
                    isLoggedIn: true,
                    username: data.user.username,
                    token, // Save the token here
                    isAdmin: hasAdminStatus,
                });

                // Optionally, save the token in localStorage or sessionStorage
                localStorage.setItem('authToken', token);

                // Navigate to the home page
                navigate('/home');
            } else {
                setMessage(data.detail || 'Invalid username or password.');
            }
        } catch (error) {
            console.error('Error checking user:', error);
            setMessage('Error logging in. Please try again.');
        }
    };


	return (
		<div className="min-h-screen flex flex-col justify-center items-center bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<div className="w-[400px] p-2 relative z-10 mb-6">
				<h3 className="text-center font-bold text-2xl">
					Welcome To
				</h3>
				<h1 className="text-center text-green-400 text-4xl">
					Radar Data Viewer
				</h1>
			</div>

			<div
				className="w-[400px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-2 relative z-10 mb-4"
				style={{
					backdropFilter: "blur(10px)",
					background: "rgba(255, 255, 255, 0.1)",
				}}
			>
				<h4 className="text-lg text-green-400 text-center">
					Login to your account
				</h4>
			</div>
			<div
				className="w-[400px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6 relative z-10"
				style={{
					backdropFilter: "blur(10px)",
					background: "rgba(255, 255, 255, 0.1)",
				}}
			>
				<form onSubmit={handleLogin} className="space-y-4">
					<div>
						<label
							htmlFor="username"
							className="block text-green-400 mb-2"
						>
							Username
						</label>
						<input
							type="text"
							id="username"
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your username"
						/>
					</div>

					<div>
						<label
							htmlFor="password"
							className="block text-green-400 mb-2"
						>
							Password
						</label>
						<input
							type="password"
							id="password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							className="w-full px-4 py-2 bg-black text-white border border-green-400 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
							placeholder="Enter your password"
						/>
					</div>

					<div>
						<button
							type="submit"
							className="w-full px-4 py-2 bg-green-400 text-black font-semibold rounded-md shadow hover:bg-green-500 transition-all duration-300"
						>
							Login
						</button>
					</div>
				</form>
			</div>
		</div>
	);
};

export default LoginPage;
