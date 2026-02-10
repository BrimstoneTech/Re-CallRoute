package com.recallroute

import android.os.Bundle
import android.widget.TextView
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.recallroute.network.NetworkMonitor

class MainActivity : AppCompatActivity() {

    private lateinit var networkStatusIndicator: View
    private lateinit var networkStatusText: TextView
    private lateinit var networkMonitor: NetworkMonitor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        networkStatusIndicator = findViewById(R.id.networkStatusStatusIndicator)
        networkStatusText = findViewById(R.id.networkStatusText)
        
        setupNetworkMonitoring()
    }

    private fun setupNetworkMonitoring() {
        networkMonitor = NetworkMonitor(this) { isOnline ->
            runOnUiThread {
                if (isOnline) {
                    networkStatusIndicator.setBackgroundColor(resources.getColor(android.R.color.holo_green_dark))
                    networkStatusText.text = "Connected: On Organization Network"
                } else {
                    networkStatusIndicator.setBackgroundColor(resources.getColor(android.R.color.holo_red_dark))
                    networkStatusText.text = "Offline / Outside Network"
                }
            }
        }
        networkMonitor.startMonitoring()
    }

    override fun onDestroy() {
        super.onDestroy()
        networkMonitor.stopMonitoring()
    }
}
