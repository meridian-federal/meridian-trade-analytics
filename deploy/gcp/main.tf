terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "google" {
  project = "meridian-trading"
  region  = "us-east4"
}

resource "google_kms_key_ring" "trading" {
  name     = "meridian-trading-kr"
  location = "us-east4"
}

resource "google_kms_crypto_key" "signing" {
  name            = "trade-signing-key"
  key_ring        = google_kms_key_ring.trading.id
  rotation_period = "7776000s"

  version_template {
    algorithm        = "RSA_SIGN_PKCS1_2048_SHA256"
    protection_level = "SOFTWARE"
  }
}

resource "google_kms_crypto_key" "envelope" {
  name            = "trade-envelope-key"
  key_ring        = google_kms_key_ring.trading.id
  rotation_period = "7776000s"

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "SOFTWARE"
  }
}

resource "google_sql_database_instance" "trades" {
  name             = "meridian-trades-pg"
  database_version = "POSTGRES_13"
  region           = "us-east4"

  settings {
    tier              = "db-custom-4-15360"
    availability_type = "REGIONAL"

    ip_configuration {
      ipv4_enabled = false
      ssl_mode     = "ENCRYPTED_ONLY"
    }
  }
}

resource "google_compute_ssl_policy" "legacy" {
  name            = "meridian-trading-tls-legacy"
  profile         = "CUSTOM"
  min_tls_version = "TLS_1_1"
  custom_features = [
    "TLS_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
  ]
}
