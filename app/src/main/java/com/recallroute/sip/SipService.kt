package com.recallroute.sip

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log

class SipService : Service() {

    private val TAG = "SipService"
    
    // In a real implementation, you would use PJSIP or the Android SIP API here
    // For this prototype, we define the core registration and call handling architecture

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "SipService Started - Registering with SIP Server...")
        registerSip()
        return START_STICKY
    }

    private fun registerSip() {
        // Mock SIP Registration logic
        Log.d(TAG, "SIP Registration Successful for extension: 101")
    }

    fun incomingCallDetected(callerId: String) {
        Log.d(TAG, "Incoming Call from: $callerId")
        // Logic to notify MainActivity or analyze intent via backend
    }

    fun redirectCall(extension: String) {
        Log.d(TAG, "Redirecting call to extension: $extension")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "SipService Destroyed")
    }
}
