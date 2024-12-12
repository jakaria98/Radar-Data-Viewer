import React from "react";

const Header = () => {
	const handleLogout = () => {
		// logout code
	};

	return (
		<header className="bg-headerFooter border-b-2 border-green-400 py-4 z-0">
			<div className="px-4 flex justify-between">
				<h1 className="text-4xl font-bold text-green-400">
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
