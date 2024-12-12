import React from "react";
import { useAuth } from "./AuthContext";

const ProtectedRoute = ({ children }) => {
	const { authState } = useAuth();

	if (!authState.isLoggedIn) {
		return <Navigate to="/login" />;
	}

	return children;
};

export default ProtectedRoute;
