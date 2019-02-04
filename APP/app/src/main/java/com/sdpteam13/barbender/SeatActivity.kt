package com.sdpteam13.barbender

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.widget.*
import com.google.android.gms.common.api.CommonStatusCodes
import com.google.android.gms.vision.barcode.Barcode
import com.sdpteam13.barbender.barcode.BarcodeCaptureActivity

class SeatActivity : AppCompatActivity() {

    private lateinit var mResultTextView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_seat)

        mResultTextView = findViewById(R.id.result_textview)

        findViewById<ImageView>(R.id.scan_barcode_button).setOnClickListener {
            val intent = Intent(applicationContext, BarcodeCaptureActivity::class.java)
            startActivityForResult(intent, BARCODE_READER_REQUEST_CODE)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == BARCODE_READER_REQUEST_CODE) {
            if (resultCode == CommonStatusCodes.SUCCESS) {
                if (data != null) {
                    val barcode = data.getParcelableExtra<Barcode>(BarcodeCaptureActivity.BarcodeObject)
                    val p = barcode.cornerPoints
                    if (barcode.displayValue.equals("1") or barcode.displayValue.equals("2") or barcode.displayValue.equals("1")) {
                        Toast.makeText(this, "Order Confirmed!", Toast.LENGTH_LONG).show()
                        mResultTextView.text = "Seat number: " + barcode.displayValue + "\n\n I won't be long now...please feel free to order again at any time!"
                        /** display string of the result: mResultTextView.text = barcode.displayValue */
                        val intent2 = Intent(applicationContext, MainActivity::class.java)
                        intent2.putExtra("Seat", barcode.displayValue)
                        startActivity(intent2)
                    }else
                        mResultTextView.setText("Not a valid QR code, please scan the code on your seat")

                } else
                    mResultTextView.setText("No barcode captured")
            } else
                Log.e(LOG_TAG, String.format(getString(R.string.barcode_error_format),
                        CommonStatusCodes.getStatusCodeString(resultCode)))
        } else
            super.onActivityResult(requestCode, resultCode, data)
    }

    companion object {
        private val LOG_TAG = MainActivity::class.java.simpleName
        private val BARCODE_READER_REQUEST_CODE = 1
    }
}