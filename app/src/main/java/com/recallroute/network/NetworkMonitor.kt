package com.recallroute.network

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest

class NetworkMonitor(
    private val context: Context,
    private val onStatusChange: (Boolean) -> Unit
) {
    private val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    
    private val networkCallback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            onStatusChange(isOrganizationNetwork())
        }

        override fun onLost(network: Network) {
            onStatusChange(false)
        }
        
        override fun onCapabilitiesChanged(network: Network, capabilities: NetworkCapabilities) {
            onStatusChange(isOrganizationNetwork())
        }
    }

    fun startMonitoring() {
        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()
        connectivityManager.registerNetworkCallback(request, networkCallback)
        onStatusChange(isOrganizationNetwork()) // Initial check
    }

    fun stopMonitoring() {
        connectivityManager.unregisterNetworkCallback(networkCallback)
    }

    private fun isOrganizationNetwork(): Boolean {
        // In a real scenario, this would check for specific IP ranges or VPN status
        val activeNetwork = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork) ?: return false
        
        // Basic check for Wi-Fi or Ethernet (common for LAN/Office)
        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) || 
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) ||
               capabilities.hasTransport(NetworkCapabilities.TRANSPORT_VPN)
    }
}
