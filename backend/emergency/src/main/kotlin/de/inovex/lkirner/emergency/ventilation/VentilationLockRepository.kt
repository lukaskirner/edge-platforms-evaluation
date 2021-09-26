package de.inovex.lkirner.emergency.ventilation

import org.springframework.data.repository.CrudRepository
import org.springframework.stereotype.Repository

@Repository
interface VentilationLockRepository: CrudRepository<VentilationLock, String>
