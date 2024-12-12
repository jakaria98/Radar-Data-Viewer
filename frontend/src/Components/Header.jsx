import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const Header = () => {
	const { logout } = useAuth();
	const navigate = useNavigate();

	const handleLogout = () => {
		logout();
		navigate("/login");
	};

	return (
		<header className="bg-headerFooter border-b-2 border-green-400 py-4 sticky top-0 w-full z-10">
			<div className="px-4 flex justify-between">
				<h1 className="text-3xl font-bold text-green-400">
					Radar Data Viewer
				</h1>
				<button className="glass-button" onClick={handleLogout}>
					Logout
				</button>
			</div>
		</header>
	);
};

export default Header;
